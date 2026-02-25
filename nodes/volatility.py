import numpy as np
from state import State

def volatility_node(state: State) -> dict:
    """
    Node c — Calculates volatility, Sharpe ratio, and correlation matrix.
    Runs in parallel with node b (market risk).
    """

    # reads the data node A already prepared
    portfolio = state["portfolio"]
    price_history = state["price_history"]

    print("[Node C] Starting volatility and correlation calculations...")

    # Calculate daily returns for each asset 
    # Same logic as node b — we need percentage changes, not raw prices

    daily_returns = {}
    for asset, prices in price_history.items():
        returns = [
            (prices[i] - prices[i-1]) / prices[i-1] 
            for i in range(1, len(prices))
        ]
        daily_returns[asset] = returns

    if not daily_returns:
        raise ValueError("No valid assets with sufficient price data.")

    
    # Calculate annualized volatility for each asset
    # Volatility = standard deviation of daily returns × √252
    # 252 is the number of trading days in a year
    # Annualizing lets us compare volatility across different time horizons

    volatility_scores = {}
    for asset, returns in daily_returns.items():
        daily_std = np.std(returns)  # how much returns vary day to day
        annualized_volatility = daily_std * np.sqrt(252) # scale up to a full year
        volatility_scores[asset] = float(round(annualized_volatility, 4))

    print(f"[Node C] Volatility scores: {volatility_scores}")
    # filters out NaN scores from failed assets
    volatility_scores = {
        asset: score
        for asset, score in volatility_scores.items()
        if not np.isnan(score)
    }

    # Calculate portfolio Sharpe Ratio
    # Sharpe Ratio measures return per unit of risk
    # Formula: (average portfolio return - risk free rate) / portfolio std deviation
    # We use 0.04 (4%) as the annual risk-free rate (approximates US Treasury bonds)
    risk_free_rate_daily = 0.04 / 252      # convert annual rate to daily

    # only uses assets that actually exist in price_history
    available_assets = {asset: weight for asset, weight in portfolio.items() 
                    if asset in daily_returns}

    num_days = min(len(returns) for returns in daily_returns.values())
    portfolio_returns = []

    for i in range(num_days):
        daily_portfolio_return = sum(
            daily_returns[asset][i] * available_assets[asset]
            for asset in available_assets
        )
        portfolio_returns.append(daily_portfolio_return)


    # Average daily return of the whole portfolio
    avg_portfolio_return = np.mean(portfolio_returns)

    # Standard deviation of portfolio returns (overall portfolio risk)
    portfolio_std = np.std(portfolio_returns)

    # Annualized Sharpe Ratio
    # Multiply by √252 to scale from daily to annual
    sharpe_ratio = (
        (avg_portfolio_return - risk_free_rate_daily) / portfolio_std * np.sqrt(252)
        if portfolio_std != 0 else 0.0       # avoid division by zero
    )
    sharpe_ratio = float(round(sharpe_ratio, 4))

    print(f"[Node C] Sharpe Ratio: {sharpe_ratio}")


    # Calculate the Correlation Matrix 
    # Correlation tells us how assets move relative to each other
    # Range: -1 (opposite directions) to +1 (identical movements)
    # A diversified portfolio should have LOW correlation between assets
    assets = list(daily_returns.keys())

    # Build a 2D dict to store correlation between every pair of assets
    correlation_matrix = {}
    for asset_a in assets:
        correlation_matrix[asset_a] = {}
        for asset_b in assets:
            # np.corrcoef returns a 2x2 matrix, we take the [0][1] value
            # which is the correlation between the two assets
            corr = np.corrcoef(daily_returns[asset_a], daily_returns[asset_b])[0][1]
            correlation_matrix[asset_a][asset_b] = float(round(corr, 4))

    print(f"[Node C] Correlation matrix calculated for {len(assets)} assets.")

    # Return only the fields this node is responsible for
    return {
        "volatility_scores": volatility_scores,
        "sharpe_ratio": sharpe_ratio,
        "correlation_matrix": correlation_matrix
    }