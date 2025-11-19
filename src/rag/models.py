"""
RAG Models
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RAGConfig(BaseModel):
    """
    Configuration for RAG module.
    """
    # Vector store settings
    persist_directory: str = Field("./data/vector_db", description="Directory to persist vector store")
    collection_name: str = Field("sql_schema", description="Name of the collection")
    
    # Embedding settings
    embedding_model: str = Field("all-MiniLM-L6-v2", description="HuggingFace embedding model name")
    
    # Search settings
    top_k: int = Field(5, description="Number of results to return")
    similarity_threshold: float = Field(0.7, description="Similarity threshold for filtering")

@dataclass
class Document:
    """
    Represents a document to be indexed or retrieved.
    """
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None
    score: Optional[float] = None  # Similarity score
