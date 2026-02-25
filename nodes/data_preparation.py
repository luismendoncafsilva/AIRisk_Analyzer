from state import State
from tools.price_simulator import fetch_historical_prices

def data_preparation_node(state: State) -> dict:
    """ Node A fetches historical price data for all assets in the portfolio. 
    Runs first before the parallel nodes"""

    # Reads the users input from the shared state
    portfolio = state["portfolio"]
    time_horizon = state["time_horizon"]
    print(f"[Node A] Fetching historical prices for: {list(portfolio.keys())})")

    # Call our yfinance tool to fetch closing prices for each asset
    price_history = fetch_historical_prices(portfolio, time_horizon)
    print(f"[Node A] Successfully fetched {time_horizon} days of data for {len(price_history)} assets.")

    return {"price_history": price_history}
