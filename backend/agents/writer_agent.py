from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.config import settings
from backend.agents.state import ResearchState

def writer_node(state: ResearchState) -> dict:
    print("--- WRITING REPORT ---")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=settings.GEMINI_API_KEY)
    
    summaries = "\n".join(state.get("summaries", []))
    feedback = state.get("critic_feedback", "")
    
    if not feedback:
        prompt = f"""
        You are an expert research writer. Write a comprehensive, well-structured markdown report on the topic: '{state["topic"]}'.
        Use the following summaries as your source material. Do not hallucinate information outside of these summaries.
        
        Summaries:
        {summaries}
        
        Structure your report with:
        - Introduction
        - Key Findings
        - Detailed Analysis
        - Conclusion
        """
    else:
        prompt = f"""
        You are an expert research writer. You need to revise your previous report on the topic: '{state["topic"]}'.
        
        Previous Draft:
        {state["draft_report"]}
        
        Critic Feedback to Address:
        {feedback}
        
        Please rewrite the report to address all of the critic's feedback. Output the full revised markdown report.
        """
        
    response = llm.invoke(prompt)
    
    # Increment revision count
    current_revisions = state.get("revision_count", 0)
    
    return {"draft_report": response.content, "revision_count": current_revisions + 1}
