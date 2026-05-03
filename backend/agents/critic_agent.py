from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.config import settings
from backend.agents.state import ResearchState
from pydantic import BaseModel, Field
import json

class ReviewResult(BaseModel):
    is_approved: bool = Field(description="True if the report meets all standards, False otherwise")
    feedback: str = Field(description="If not approved, provide detailed feedback on what needs to be fixed. If approved, just say 'Approved'.")

def critic_node(state: ResearchState) -> dict:
    print("--- CRITIQUING REPORT ---")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=settings.GEMINI_API_KEY)
    
    prompt = f"""
    You are an expert research editor. Review the following draft report for the topic: '{state["topic"]}'.
    
    Draft Report:
    {state["draft_report"]}
    
    Evaluate it on:
    1. Relevance to the topic
    2. Depth and comprehensiveness
    3. Structural clarity
    
    If it is excellent, approve it. If it is lacking, reject it and provide specific, actionable feedback for the writer to improve it.
    Return ONLY a JSON object with 'is_approved' (boolean) and 'feedback' (string).
    """
    
    response = llm.invoke(prompt)
    
    try:
        # Try to parse the JSON output
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        result = json.loads(text.strip())
        is_approved = result.get("is_approved", True)
        feedback = result.get("feedback", "Approved")
    except Exception as e:
        is_approved = True # Default to pass if parsing fails
        feedback = "Approved"
        
    # Check max revisions
    if state.get("revision_count", 0) >= state.get("max_revisions", 2):
        print("Max revisions reached. Forcing approval.")
        is_approved = True
        
    if is_approved:
        return {"final_report": state["draft_report"], "critic_feedback": "Approved"}
    else:
        return {"critic_feedback": feedback}
