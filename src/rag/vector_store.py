"""
Vector Store Service
"""
import chromadb
from chromadb.config import Settings
from typing import List, Optional
from .models import RAGConfig, Document
from .embedding_service import EmbeddingService

class VectorStore:
    """
    Manages interaction with ChromaDB vector store.
    """

    def __init__(self, config: RAGConfig, embedding_service: EmbeddingService):
        self.config = config
        self.embedding_service = embedding_service
        self._client = chromadb.PersistentClient(path=self.config.persist_directory)
        self._collection = self._client.get_or_create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Document]):
        """
        Add documents to the vector store.
        """
        if not documents:
            return

        ids = [doc.id or f"doc_{i}" for i, doc in enumerate(documents)]
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        # Generate embeddings
        embeddings = self.embedding_service.embed_documents(texts)

        self._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings, # type: ignore
            metadatas=metadatas # type: ignore
        )

    def query(self, query_text: str, n_results: Optional[int] = None) -> List[Document]:
        """
        Query the vector store for similar documents.
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
                    metadata=results['metadatas'][0][i] if results['metadatas'] else {},
                    id=results['ids'][0][i],
                    score=results['distances'][0][i] if results['distances'] else None
                )
                documents.append(doc)

        return documents

    def delete_collection(self):
        """
        Delete the entire collection (useful for testing/reset).
        """
        self._client.delete_collection(self.config.collection_name)
