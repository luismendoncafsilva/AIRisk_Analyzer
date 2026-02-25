from typing import Any, Dict, List, Optional, Annotated
from langgraph.graph import MessagesState
import operator

class State(MessagesState):

    # --- Input ---
    portfolio: Dict
    time_horizon: int

    # --- Node a output ---
    price_history: Optional[Dict] = None

    # --- Node b output ---
    value_at_risk: Optional[float] = None
    stress_test_results: Optional[str] = None

    # --- Node c output ---
    volatility_scores: Optional[dict] = None
    sharpe_ratio: Optional[float] = None
    correlation_matrix: Optional[dict] = None

    # --- Node d output ---
    final_report: Optional[str] = None
    risk_rating: Optional[str] = None