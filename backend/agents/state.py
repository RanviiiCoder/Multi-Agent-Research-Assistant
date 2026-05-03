from typing import TypedDict, List, Annotated
import operator

class ResearchState(TypedDict):
    topic: str
    search_queries: List[str]
    search_results: Annotated[List[dict], operator.add]
    summaries: Annotated[List[str], operator.add]
    draft_report: str
    critic_feedback: str
    revision_count: int
    max_revisions: int
    final_report: str
