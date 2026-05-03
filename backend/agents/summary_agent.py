from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.config import settings
from backend.agents.state import ResearchState
from backend.vector_store.faiss_store import vector_db

def summary_node(state: ResearchState) -> dict:
    print("--- SUMMARIZING ---")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=settings.GEMINI_API_KEY)
    
    # Retrieve top relevant docs for the topic
    docs = vector_db.search(state["topic"], k=5)
    
    if not docs:
        return {"summaries": ["No substantial information found to summarize."]}

    # Combine docs into a single context block
    context = "\n\n".join([f"Source ({d.metadata.get('title', 'Unknown')}): {d.page_content}" for d in docs])
    
    prompt = f"""
    You are an expert summarizer. Based on the following raw search results, extract the most important facts, data points, and context regarding the topic: '{state["topic"]}'.
    
    Search Results:
    {context}
    
    Write a comprehensive, bulleted summary.
    """
    
    response = llm.invoke(prompt)
    return {"summaries": [response.content]}
