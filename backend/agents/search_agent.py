from duckduckgo_search import DDGS
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.core.config import settings
from backend.agents.state import ResearchState
from backend.vector_store.faiss_store import vector_db
import json

def generate_search_queries(topic: str) -> list[str]:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=settings.GEMINI_API_KEY)
    prompt = f"You are a research assistant. Generate 3 distinct search queries to thoroughly research the following topic: '{topic}'. Return ONLY a JSON list of strings."
    
    response = llm.invoke(prompt)
    try:
        # Try to parse the JSON output
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        queries = json.loads(text.strip())
        return queries
    except Exception as e:
        # Fallback if parsing fails
        return [topic, f"What is {topic}", f"{topic} overview"]

def search_node(state: ResearchState) -> dict:
    print(f"--- SEARCHING FOR: {state['topic']} ---")
    queries = generate_search_queries(state["topic"])
    
    all_results = []
    with DDGS() as ddgs:
        for query in queries:
            results = list(ddgs.text(query, max_results=3))
            all_results.extend(results)
    
    # Store in Vector DB for summarize agent
    texts = []
    metadatas = []
    for r in all_results:
        texts.append(r.get("body", ""))
        metadatas.append({"title": r.get("title", ""), "href": r.get("href", "")})
    
    if texts:
        vector_db.add_texts(texts, metadatas)
        
    return {"search_queries": queries, "search_results": all_results}
