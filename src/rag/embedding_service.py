"""
Embedding Service
"""
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from .models import RAGConfig

class EmbeddingService:
    """
    Generates embeddings for text using SentenceTransformers.
    """
    
    def __init__(self, config: RAGConfig):
        self.config = config
        self._model: Optional[SentenceTransformer] = None

    @property
    def model(self) -> SentenceTransformer:
        """
        Lazy load the model.
        """
        if self._model is None:
            self._model = SentenceTransformer(self.config.embedding_model)
        return self._model

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.
        """
        embeddings = self.model.encode([text])
        return embeddings[0].tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
