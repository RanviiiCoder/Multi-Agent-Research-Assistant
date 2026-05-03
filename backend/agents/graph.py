from langgraph.graph import StateGraph, END
from backend.agents.state import ResearchState
from backend.agents.search_agent import search_node
from backend.agents.summary_agent import summary_node
from backend.agents.writer_agent import writer_node
from backend.agents.critic_agent import critic_node
from backend.vector_store.faiss_store import vector_db

def route_after_critic(state: ResearchState):
    """Routing logic: If approved or max revisions hit, end. Else, rewrite."""
    if state.get("critic_feedback") == "Approved":
        return "end"
    return "rewrite"

def build_graph() -> StateGraph:
    # 1. Initialize State Graph
    workflow = StateGraph(ResearchState)
    
    # 2. Add Nodes
    workflow.add_node("search", search_node)
    workflow.add_node("summarize", summary_node)
    workflow.add_node("write", writer_node)
    workflow.add_node("critic", critic_node)
    
    # 3. Add Edges
    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarize")
    workflow.add_edge("summarize", "write")
    workflow.add_edge("write", "critic")
    
    # Conditional edge from critic
    workflow.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "end": END,
            "rewrite": "write"
        }
    )
    
    # 4. Compile Graph
    return workflow.compile()

graph = build_graph()

def run_research(topic: str, max_revisions: int = 2) -> dict:
    """Entry point to run the graph."""
    # Clear vector db for new research
    vector_db.clear()
    
    initial_state = {
        "topic": topic,
        "search_queries": [],
        "search_results": [],
        "summaries": [],
        "draft_report": "",
        "critic_feedback": "",
        "revision_count": 0,
        "max_revisions": max_revisions,
        "final_report": ""
    }
    
    # Execute the graph
    result = graph.invoke(initial_state)
    return result
