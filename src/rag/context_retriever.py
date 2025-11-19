"""
Context Retriever Service
"""
from typing import List
from .models import RAGConfig, Document
from .vector_store import VectorStore

class ContextRetriever:
    """
    Retrieves relevant context for a given query.
    """
    
    def __init__(self, config: RAGConfig, vector_store: VectorStore):
        self.config = config
        self.vector_store = vector_store

    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents for the query.
        """
        # In the future, this could include hybrid search, re-ranking, etc.
        return self.vector_store.query(
            query_text=query,
            n_results=self.config.top_k
        )

    def format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into a single context string.
        """
        context_parts = []
        for doc in documents:
            # Format based on metadata type if available
            doc_type = doc.metadata.get('type', 'unknown')
            if doc_type == 'table':
                context_parts.append(f"Table Schema: {doc.content}")
            elif doc_type == 'column':
                context_parts.append(f"Column Description: {doc.content}")
            else:
                context_parts.append(doc.content)
                
        return "\n\n".join(context_parts)
