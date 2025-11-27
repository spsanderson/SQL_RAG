"""
Vector Store Service.

Manages interaction with ChromaDB for vector-based document storage and retrieval.
"""
from typing import List, Optional

import chromadb

from .embedding_service import EmbeddingService
from .models import Document, RAGConfig


class VectorStore:
    """Manages interaction with ChromaDB vector store."""

    def __init__(self, config: RAGConfig, embedding_service: EmbeddingService):
        """
        Initialize the vector store.

        Args:
            config: RAG configuration settings.
            embedding_service: Service for generating embeddings.
        """
        self.config = config
        self.embedding_service = embedding_service
        self._client = chromadb.PersistentClient(
            path=self.config.persist_directory
        )
        self._collection = self._client.get_or_create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.

        Args:
            documents: List of documents to add.
        """
        if not documents:
            return

        ids = [doc.id or f"doc_{i}" for i, doc in enumerate(documents)]
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        embeddings = self.embedding_service.embed_documents(texts)

        self._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,  # type: ignore
            metadatas=metadatas  # type: ignore
        )

    def query(
        self,
        query_text: str,
        n_results: Optional[int] = None
    ) -> List[Document]:
        """
        Query the vector store for similar documents.

        Args:
            query_text: The query string to search for.
            n_results: Optional number of results to return.

        Returns:
            List of matching documents with similarity scores.
        """
        n_results = n_results or self.config.top_k
        query_embedding = self.embedding_service.embed_query(query_text)

        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        documents = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                doc = Document(
                    content=results['documents'][0][i],
                    metadata=(
                        results['metadatas'][0][i]
                        if results['metadatas'] else {}
                    ),
                    id=results['ids'][0][i],
                    score=(
                        results['distances'][0][i]
                        if results['distances'] else None
                    )
                )
                documents.append(doc)

        return documents

    def delete_collection(self) -> None:
        """Delete the entire collection (useful for testing/reset)."""
        self._client.delete_collection(self.config.collection_name)
