from langgraph.graph import StateGraph, START, END
from state import State
from nodes.data_preparation import data_preparation_node
from nodes.market_risk import market_risk_node
from nodes.volatility import volatility_node
from nodes.report_synthesis import report_synthesis_node

def risk_analyzer_graph():
    """  Builds and compiles the portfolio risk analyzer graph."""


    # Initialize the graph with our shared state 
    # This tells LangGraph what data structure flows between all nodes
    graph = StateGraph(State)

    # Add nodes to the graph
    graph.add_node("data preparation", data_preparation_node)
    graph.add_node("market risk", market_risk_node)
    graph.add_node("volatility", volatility_node)
    graph.add_node("report synthesis", report_synthesis_node)

    # Define the edges
    graph.add_edge(START, "data preparation")  # Start -> Node A
    graph.add_edge("data preparation", "market risk")  # Node A -> Node B
    graph.add_edge("data preparation", "volatility")  # Node A -> Node C
    graph.add_edge("market risk", "report synthesis")  # Node B -> Node D
    graph.add_edge("volatility", "report synthesis")  # Node C -> Node D

    graph.add_edge("report synthesis", END)  # Node D -> End

    # Compile the graph 
    app = graph.compile()
    return app