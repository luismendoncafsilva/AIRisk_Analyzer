import yfinance as yf
import time
from datetime import datetime, timedelta

def fetch_historical_prices(portfolio: dict, time_horizon: int) -> dict:
    """ 
    Fetches real daily closing prices for each asset using yfinance.

    Args:
        portfolio: dict of asset -> allocation, e.g. {"AAPL": 0.4, "GOOGL": 0.3}
        time_horizon: number of days to look back
        Returns:
            Dict of asset -> list of daily closing prices"""
    
    end_date = datetime.today()
    start_date = end_date - timedelta(days=time_horizon)

    # This dict will hold the results
    price_history = {}

    for asset in portfolio.keys():
        ticker = yf.Ticker(asset)    # Create a yf Ticker object for this asset

        # Download all tickers at once
        # Fetch the historical price data as a DataFrame
        # .strftime("%Y-%m-%d") converts the date to the format yfinance expects " 2024-01-15"
        tickers = list(portfolio.keys())
        df = yf.download(
            tickers,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            auto_adjust=True
        )

        #If the DataFrame is empty, the ticker symbol is likely invalid
        # We raise an error early so the user knows exactly what went wrong
        if df.empty:
            raise ValueError(f"No data found for asset: {asset}. Check the ticker symbol.")
        # Extract only the "Close" column (closing price of each day)
        price_history = {}
        for asset in tickers:
            try:
                asset_prices = df["Close"][asset].dropna().tolist()
                if len(asset_prices) < 2:
                    print(f"[Node A] Skipping {asset} — insufficient data.")
                    continue
                price_history[asset] = [round(p, 2) for p in asset_prices]
            except KeyError:
                print(f"[Node A] Skipping {asset} — not found in downloaded data.")
                continue

        # Small delay between requests to avoid yfinance rate limiting
        time.sleep(1)

        return price_history


def fetch_stress_test_history(portfolio: dict, years: int = 3) -> dict:
    """ Fetches a longer price history specifically for the historical stress test.
    
    Args:
        portfolio: dict of asset -> allocation
        years: number of years to look back (default 3)

    Returns:
        dict of asset -> list of daily closing prices
    """

    end_date = datetime.today()
    # Convert years to days (365 * years)
    start_date = end_date - timedelta(days=365 * years)

    tickers = list(portfolio.keys())

    df = yf.download(
        tickers,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        auto_adjust=True
    )

    if df.empty:
        raise ValueError("No stress test data returned. Check your ticker symbols.")

    stress_history = {}
    for asset in tickers:
        asset_prices = df["Close"][asset].dropna().tolist()
        stress_history[asset] = [round(p, 2) for p in asset_prices]

    # Also store the actual trading dates for reporting
    stress_history["_dates"] = df.index.strftime("%Y-%m-%d").tolist()

    return stress_history

