import argparse
import time
import random
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import os

# --- DATABASE CONFIGURATION ---
# Use environment variables for security to avoid leaking credentials on GitHub
DB_USER = os.getenv('DB_USER', 'your_username')
DB_PASS = os.getenv('DB_PASS', 'your_password')
DB_HOST = os.getenv('DB_HOST', 'your_hostname')
DB_NAME = os.getenv('DB_NAME', 'your_dbname')

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

def get_sp500_tickers():
    """Extract current S&P 500 symbols from Wikipedia"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        tickers = []
        for row in table.find_all('tr')[1:]:
            ticker = row.find_all('td')[0].text.strip()
            # Yahoo Finance compatibility
            tickers.append(ticker.replace('.', '-'))
        return tickers
    except Exception as e:
        print(f"Error fetching tickers: {e}")
        return []

def run_etl_pipeline(start_date, end_date, intervals=['1d', '1wk', '1mo']):
    """Main ETL logic: Fetching and storing data into separate tables based on interval"""
    tickers = get_sp500_tickers()
    if not tickers:
        return

    engine = create_engine(DB_URL)

    for interval in intervals:
        # Determine specific table name for this interval
        table_name = f"stock_prices_{interval}"
        print(f"\n>>> Starting collection for Table: {table_name}")

        for symbol in tickers:
            try:
                ticker_obj = yf.Ticker(symbol)
                df = ticker_obj.history(start=start_date, end=end_date, interval=interval)
                
                # Check if df is empty or entirely NaN
                if df.empty or df['Close'].isnull().all():
                    print(f"  [Skip] {symbol}: No valid data found.")
                    continue
                
                # Cleaning and formatting
                df = df.dropna(subset=['Close']).reset_index()
                df.columns = [c.lower() for c in df.columns]
                df['symbol'] = symbol
                df['date'] = pd.to_datetime(df['date']).dt.date
                
                # Select core columns (excluding 'interval' column as it's now implied by the table name)
                final_df = df[['symbol', 'date', 'open', 'close', 'high', 'low', 'volume', 'dividends']]
                
                # Load into interval-specific table
                final_df.to_sql(table_name, engine, if_exists='append', index=False)
                print(f"  [Success] {symbol} data pushed to {table_name}.")
                
                # Rate limiting to prevent IP blocking
                time.sleep(random.uniform(0.5, 1.2))
                
            except Exception as e:
                print(f"  [Error] {symbol} failed: {e}")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-interval S&P 500 Data Pipeline")
    parser.add_argument("--start", type=str, required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", type=str, required=True, help="YYYY-MM-DD")
    
    args = parser.parse_args()
    
    # You can customize the interval list here
    run_etl_pipeline(args.start, args.end, intervals=['1d', '1wk', '1mo'])