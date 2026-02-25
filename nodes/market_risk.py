import numpy as np
from state import State
from tools.price_simulator import fetch_historical_prices, fetch_stress_test_history

def market_risk_node(state: State) -> dict:
    """
    Node b — Calculates Value at Risk (VaR) and runs a
    historical simulation stress test over the last 3 years.
    Runs in parallel with node c (volatility).
    """

    portfolio = state["portfolio"]
    price_history = state["price_history"]

    print("[Node B] Starting market risk calculations...")

    # PART 1: Value at Risk (VaR)
    # Uses the short-term price history from node a (e.g. 90 days)

    # Calculate daily returns for each asset
    daily_returns = {}
    for asset, prices in price_history.items():
        returns = [
            (prices[i] - prices[i - 1]) / prices[i - 1]
            for i in range(1, len(prices))
        ]
        daily_returns[asset] = returns

    # Only use assets successfully fetched by yfinance
    available_assets = {asset: weight for asset, weight in portfolio.items()
                        if asset in daily_returns}

    # Calculate weighted portfolio daily returns
    num_days = min(len(returns) for returns in daily_returns.values())
    portfolio_returns = []

    for i in range(num_days):
        daily_portfolio_return = sum(
            daily_returns[asset][i] * available_assets[asset]
            for asset in available_assets
        )
        portfolio_returns.append(daily_portfolio_return)

    # VaR at 95% confidence — worst loss on 95% of days
    var_95 = np.percentile(portfolio_returns, 5)
    value_at_risk = float(round(abs(var_95), 4))

    print(f"[Node B] Value at Risk (95%): {value_at_risk * 100:.2f}%")

    # PART 2: Historical Simulation Stress Test
    # Fetches 3 years of real data and finds the
    # worst 30, 60, and 90 day rolling windows

    print("[Node B] Fetching 3 years of data for stress test...")

    # Fetch 3 years of real historical prices
    stress_data = fetch_stress_test_history(portfolio, years=3)

    # Extract dates and remove from asset data
    dates = stress_data.pop("_dates")

    # Calculate daily returns for the full 3-year period
    stress_returns = {}
    for asset, prices in stress_data.items():
        returns = [
            (prices[i] - prices[i - 1]) / prices[i - 1]
            for i in range(1, len(prices))
        ]
        stress_returns[asset] = returns

    # Only use assets we have stress data for
    available_stress_assets = {asset: weight for asset, weight in portfolio.items()
                                if asset in stress_returns}

    # Calculate weighted portfolio returns for the full 3-year period
    num_stress_days = len(list(stress_returns.values())[0])
    full_portfolio_returns = []

    for i in range(num_stress_days):
        daily_return = sum(
            stress_returns[asset][i] * available_stress_assets[asset]
            for asset in available_stress_assets
        )
        full_portfolio_returns.append(daily_return)

    # Find worst rolling windows
    # A rolling window cumulates returns over N consecutive days
    # e.g. worst 30-day window = the worst month in 3 years

    def worst_rolling_window(returns, window_days):
        """
        Finds the worst consecutive N-day period in the return series.
        Returns the total loss and the start date of that period.
        """
        worst_loss = 0
        worst_start_idx = 0

        for i in range(len(returns) - window_days):
            # Cumulate returns over the window
            # (1 + r1) * (1 + r2) * ... - 1 gives the total return
            window_returns = returns[i:i + window_days]
            cumulative_return = 1.0
            for r in window_returns:
                cumulative_return *= (1 + r)
            total_return = cumulative_return - 1

            # Track the worst (most negative) window
            if total_return < worst_loss:
                worst_loss = total_return
                worst_start_idx = i

        return float(round(worst_loss, 4)), worst_start_idx

    # Run the rolling window analysis for 3 timeframes
    windows = [30, 60, 90]
    stress_results = []

    for window in windows:
        loss, start_idx = worst_rolling_window(full_portfolio_returns, window)

        # Get the actual calendar date of the worst period
        # Offset by 1 since returns start from day 1 (no day 0 return)
        start_date = dates[start_idx + 1] if start_idx + 1 < len(dates) else "N/A"
        end_idx = min(start_idx + window, len(dates) - 1)
        end_date = dates[end_idx]

        stress_results.append({
            "window": window,
            "loss": loss,
            "start_date": start_date,
            "end_date": end_date
        })

        print(f"[Node B] Worst {window}-day period ({start_date} to {end_date}): "
              f"{loss * 100:.1f}%")

    # Format the stress test result as a structured string for node d
    stress_lines = ["Historical Stress Test — Worst Periods (Last 3 Years):"]
    for r in stress_results:
        stress_lines.append(
            f"  • Worst {r['window']}-day period "
            f"({r['start_date']} → {r['end_date']}): "
            f"{abs(r['loss']) * 100:.1f}% loss"
        )

    # Identify the single most vulnerable period
    worst = max(stress_results, key=lambda x: abs(x["loss"]))
    stress_lines.append(
        f"\n  Most vulnerable period: "
        f"{worst['start_date']} → {worst['end_date']} "
        f"({worst['window']}-day window, {abs(worst['loss']) * 100:.1f}% loss)"
    )

    stress_test_result = "\n".join(stress_lines)

    print("[Node B] Stress test complete.")

    return {
        "value_at_risk": value_at_risk,
        "stress_test_result": stress_test_result
    }