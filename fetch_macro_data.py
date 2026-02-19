import pandas as pd
import yfinance as yf
from fredapi import Fred

# --- CONFIGURATION ---
# Replace with your actual FRED API Key
FRED_API_KEY = "10e122d1c44ae3ebae16fe11b92a3219" 

def show_macro_data(start_date, end_date):
    """
    Fetches macro indicators and displays them as a Pandas DataFrame
    """
    try:
        fred = Fred(api_key=FRED_API_KEY)
        print(f"Fetching data from {start_date} to {end_date}...")

        # Fetching from FRED
        # CPI (Monthly), Unemployment (Monthly), Fed Funds Rate (Daily), USD Index (Daily)
        cpi = fred.get_series("CPIAUCSL", observation_start=start_date, observation_end=end_date)
        unrate = fred.get_series("UNRATE", observation_start=start_date, observation_end=end_date)
        rate = fred.get_series("DFF", observation_start=start_date, observation_end=end_date)
        usd = fred.get_series("DTWEXBGS", observation_start=start_date, observation_end=end_date)

        # Fetching VIX from Yahoo Finance
        vix_data = yf.download("^VIX", start=start_date, end=end_date)
        vix = vix_data["Close"]

        # Merge
        macro_df = pd.concat([cpi, unrate, rate, usd, vix], axis=1)
        macro_df.columns = ["CPI", "Unemployment_Rate", "Fed_Funds_Rate", "USD_Index", "VIX"]

        # 4. Frequency Alignment (Daily interpolation for missing values)
        # This fills the monthly CPI/Unemployment gaps so they align with daily Rate/VIX
        macro_df = macro_df.resample("D").interpolate(method="time")
        
        # Filter for the exact range and drop rows where essential data might be missing
        macro_df = macro_df.loc[start_date:end_date]

        # Display the result
        print("\n--- Macroeconomic Data Summary ---")
        print(macro_df.tail(10)) # Show last 10 days
        return macro_df

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

show_macro_data(start_date="2023-01-01", end_date="2024-01-01")