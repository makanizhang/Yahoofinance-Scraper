import time
import yfinance as yf
import pandas as pd
import random
import argparse

def fetch_price(symbol, interval, start_date, end_date):
    """Fetch and format stock data"""
    try:
        df = yf.Ticker(symbol).history(interval=interval, start=start_date, end=end_date)
        if df.empty:
            print(f"Warning: {symbol} ({interval}) has no data")
            return None

        df = df.reset_index()

        if "Date" in df.columns:
            df = df.rename(columns={"Date": "date"})
        elif "Datetime" in df.columns:
            df = df.rename(columns={"Datetime": "date"})
        else:
            print(f"Warning: {symbol} ({interval}) has no date column")
            return None

        df = df.rename(columns={
            "Open": "open", "Close": "close",
            "High": "high", "Low": "low",
            "Volume": "volume", "Dividends": "dividends"
        })

        df["symbol"] = symbol
        df["interval"] = interval
        df["date"] = pd.to_datetime(df["date"]).dt.date

        return df[["symbol", "date", "interval", "open", "close", "high", "low", "volume", "dividends"]]

    except Exception as e:
        print(f"Error: when fetching {symbol} ({interval}) : {str(e)}")
        return None

    
def fetch_and_store_stock_data(symbols_list, start_date, end_date, intervals, sleep_time=1, output_file="stock_data.csv"):
    """
    Fetch and store stock data to the database

    Parameters:
    symbols_list (list)
    start_date (str)
    end_date (str)
    intervals (list)
    sleep_time (int):sleep time between request
    """
    batch_data = []

    for sym in symbols_list:
        for interval in intervals:
            df = fetch_price(sym, interval, start_date, end_date)

            if df is None or df.empty:
                null_row = {
                    "symbol": sym, "interval": interval, "date": None,
                    "open": None, "high": None, "low": None,
                    "close": None, "volume": None, "dividends": None
                }
                batch_data.append(null_row)
            else:
                df["symbol"] = sym
                df["interval"] = interval
                batch_data.extend(df.to_dict(orient="records"))

        time.sleep(sleep_time)

    if batch_data:
        df_batch = pd.DataFrame(batch_data)
        df_batch.to_csv(output_file, index=False)
        print(f"\nSaved {len(df_batch)} rows to '{output_file}'")

        # summary
        symbol_counts = df_batch['symbol'].value_counts()
        print("\nSymbol counts:")
        for symbol, count in symbol_counts.items():
            print(f"{symbol}: {count} rows")

    else:
        print("No data to save.")

    print("\nData written to CSV file!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", type=str, required=True, help="SYMBOL")
    parser.add_argument("--start", type=str, required=True, help="START TIME YYYY-MM-DD")
    parser.add_argument("--end", type=str, required=True, help="END TIME YYYY-MM-DD")
    parser.add_argument("--interval", type=str, default="1d", help=" 1h/1d/1m")

    args = parser.parse_args()

    fetch_and_store_stock_data(
        symbols_list=[args.ticker],
        start_date=args.start,
        end_date=args.end,
        intervals=[args.interval]
    )
