from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from backend.core.config import settings

class FAISSStore:
    def __init__(self):
        # We need the API key to initialize the embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2", 
            google_api_key=settings.GEMINI_API_KEY
        )
        self.vector_store = None

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """Adds raw texts to the vector store."""
        documents = []
        for i, text in enumerate(texts):
            meta = metadatas[i] if metadatas else {}
            documents.append(Document(page_content=text, metadata=meta))
            
        if not self.vector_store:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)

    def search(self, query: str, k: int = 4) -> List[Document]:
        """Searches the vector store for the top k matching documents."""
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=k)

    def clear(self):
        """Clears the vector store (useful for starting a new research topic)."""
        self.vector_store = None

# Create a singleton instance
vector_db = FAISSStore()
