from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from state import State


def report_synthesis_node(state: State) -> dict:
    """ 
    Node d — Uses an LLM to synthesize all risk data into a final report.
    Runs after nodes b and c have both completed.
    """
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Read everything that nodes b and c wrote into the state
    portfolio = state.get("portfolio", {})
    value_at_risk = state.get("value_at_risk", 0.0)
    stress_test_result = state.get("stress_test_result", "")
    volatility_scores = state.get("volatility_scores", {})
    sharpe_ratio = state.get("sharpe_ratio", 0.0)
    correlation_matrix = state.get("correlation_matrix", {})

    print("[Node D] All parallel nodes complete. Synthesizing final report")

    # Format the correlation matrix for readability
    # Convert the nested dict into a clean string for the LLM prompt
    correlation_text = ""
    for asset_a, correlations in correlation_matrix.items():
        for asset_b, value in correlations.items():
            if asset_a < asset_b:   # avoid duplicates e.g. AAPL-GOOGL and GOOGL-AAPL
                correlation_text += f"  {asset_a} vs {asset_b}: {value}\n"

    # Step 2: Format volatility scores for the prompt 
    volatility_text = "\n".join(
        f"  {asset}: {score * 100:.1f}% annualized volatility"
        for asset, score in volatility_scores.items()
    )

    # Build the prompt 
    # We give the LLM all the calculated data and ask it to reason over it
    prompt = f"""
    You are a senior financial risk analyst. Based on the following quantitative 
    data, write a professional portfolio risk report and assign a final risk rating.
    
    PORTFOLIO ALLOCATIONS:
    {portfolio}

    MARKET RISK:
    - Value at Risk (95% confidence): {value_at_risk * 100:.2f}% potential daily loss
    - Stress Test: {stress_test_result}

    VOLATILITY:
    {volatility_text}

    SHARPE RATIO: {sharpe_ratio}
    (Above 1.0 = good, above 2.0 = excellent, below 0 = underperforming risk-free rate)

    ASSET CORRELATIONS:
    {correlation_text}

    Please provide:
    1. A brief executive summary (2-3 sentences)
    2. Key risk findings from the data above
    3. Diversification assessment based on the correlation matrix
    4. A final risk rating: Low, Medium, or High — with justification

    Write in a clear, professional tone suitable for an investment committee.
    End your response with a line that says exactly: RISK RATING: <Low/Medium/High>
    """

    # Call the LLM
    response = llm.invoke([HumanMessage(content=prompt)])
    report_text = response.content
    print("[Node D] Report generated successfully.")

    # Extract the risk rating from the report 
    # The LLM was instructed to end with "RISK RATING: Low/Medium/High"
    # We parse that line to get a clean rating field
    risk_rating = "Unknown"
    for line in report_text.splitlines():
        if line.startswith("RISK RATING:"):
            risk_rating = line.replace("RISK RATING:", "").strip()
            break

    print(f"[Node D] Final Risk Rating: {risk_rating}")

    # Return the final report and extracted risk rating
    return {
        "final_report": report_text,
        "risk_rating": risk_rating
    }