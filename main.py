from graph import risk_analyzer_graph
from dotenv import load_dotenv

load_dotenv()  

def main():
    """
    Entry point — defines the portfolio input and runs the risk analyzer graph.
    """

    # Define your portfolio 
    # Keys are ticker symbols (must be valid Yahoo Finance tickers)
    # Values are allocation weights — they must add up to 1.0 (100%)
    portfolio = {
        "JPM": 0.05,    # 5% JPMorgan Chase
        "XOM": 0.05,   # 5% ExxonMobil
        "JNJ": 0.1,     # 10% Johnson & Johnson
        "BRK-B": 0.1,     # 10% Gerdau
        "GS": 0.1,     # 10% Goldman Sachs
        "TSLA": 0.1,     # 10% Tesla
        "AMZN": 0.1,     # 10% Amazon
        "MSFT": 0.1,    # 10% Microsoft
        "AAPL": 0.1,    # 10% Apple
        "GOOGL": 0.1    # 10% Alphabet
    }
    # Define your time horizon 
    # How many calendar days of historical data to analyze
    time_horizon = 90   # 3 months of data

    # Build the compiled graph
    app = risk_analyzer_graph()

    # Define the initial state
    # This is the "order ticket" we hand to the graph
    # Only the input fields are needed — everything else gets filled by the nodes
    initial_state = {
        "portfolio": portfolio,
        "time_horizon": time_horizon
    }

    print("=" * 60)
    print("   PORTFOLIO RISK ANALYZER — Starting...")
    print("=" * 60)

    # Run the graph 
    # .invoke() runs the graph synchronously and returns the final state
    # The final state contains everything — inputs + all computed fields
    final_state = app.invoke(initial_state)

    # Display the results
    print("\n" + "=" * 60)
    print("   FINAL RISK REPORT")
    print("=" * 60)
    print(final_state["final_report"])


if __name__ == "__main__":
    main()