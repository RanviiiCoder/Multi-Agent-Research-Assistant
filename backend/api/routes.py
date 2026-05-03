from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.agents.graph import run_research

router = APIRouter()

class ResearchRequest(BaseModel):
    topic: str
    max_revisions: int = 2

class ResearchResponse(BaseModel):
    topic: str
    report: str
    revisions: int

@router.post("/research", response_model=ResearchResponse)
async def generate_research_report(request: ResearchRequest):
    try:
        # Run the LangGraph workflow synchronously for simplicity in this MVP
        result = run_research(request.topic, request.max_revisions)
        
        final_report = result.get("final_report")
        if not final_report:
            final_report = result.get("draft_report", "Failed to generate report.")
            
        return ResearchResponse(
            topic=request.topic,
            report=final_report,
            revisions=result.get("revision_count", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
