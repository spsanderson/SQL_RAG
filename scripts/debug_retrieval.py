import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.rag.models import RAGConfig
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore
from src.rag.context_retriever import ContextRetriever

def debug_retrieval():
    print("Debugging Retrieval...")
    
    rag_config = RAGConfig(persist_directory="./data/vector_db_demo")
    embedding_service = EmbeddingService(rag_config)
    vector_store = VectorStore(rag_config, embedding_service)
    context_retriever = ContextRetriever(rag_config, vector_store)
    
    query = "Show me visits where the length of stay is greater than 10 days."
    print(f"\nQuery: {query}")
    
    context = context_retriever.retrieve(query)
    print(f"\nRetrieved Context:\n{context}")

if __name__ == "__main__":
    debug_retrieval()
