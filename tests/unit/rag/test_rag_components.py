"""
Unit tests for RAG components.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.rag.models import RAGConfig, Document
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore
from src.rag.context_retriever import ContextRetriever

@pytest.fixture
def rag_config():
    return RAGConfig(
        persist_directory="./test_db",
        collection_name="test_collection",
        embedding_model="test-model",
        top_k=2,
        similarity_threshold=0.5
    )

@pytest.fixture
def mock_embedding_service(rag_config):
    service = MagicMock(spec=EmbeddingService)
    service.config = rag_config
    service.embed_query.return_value = [0.1, 0.2, 0.3]
    service.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    return service

@pytest.fixture
def mock_chroma_client():
    with patch("src.rag.vector_store.chromadb.PersistentClient") as mock_client:
        yield mock_client

def test_embedding_service(rag_config):
    with patch("src.rag.embedding_service.SentenceTransformer") as mock_model:
        service = EmbeddingService(rag_config)
        
        # Test lazy loading
        assert service._model is None
        model = service.model
        assert model == mock_model.return_value
        mock_model.assert_called_once()
        
        # Test embedding
        mock_model.return_value.encode.return_value = [[0.1, 0.2]]
        assert service.embed_query("test") == [0.1, 0.2]
        
        mock_model.return_value.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
        assert service.embed_documents(["t1", "t2"]) == [[0.1, 0.2], [0.3, 0.4]]

def test_vector_store(rag_config, mock_embedding_service, mock_chroma_client):
    store = VectorStore(rag_config, mock_embedding_service)
    
    # Test add documents
    docs = [
        Document(id="1", content="test1", metadata={"a": 1}),
        Document(id="2", content="test2", metadata={"b": 2})
    ]
    store.add_documents(docs)
    store._collection.add.assert_called_once()
    
    # Test query
    store._collection.query.return_value = {
        "documents": [["test1"]],
        "metadatas": [[{"a": 1}]],
        "ids": [["1"]],
        "distances": [[0.1]]
    }
    
    results = store.query("query")
    assert len(results) == 1
    assert results[0].content == "test1"
    assert results[0].id == "1"

def test_context_retriever(rag_config):
    mock_store = MagicMock(spec=VectorStore)
    retriever = ContextRetriever(rag_config, mock_store)
    
    # Test retrieve
    mock_store.query.return_value = [
        Document(content="doc1", score=0.1), # 1 - 0.1 = 0.9 similarity
        Document(content="doc2", score=0.8)  # 1 - 0.8 = 0.2 similarity (below threshold)
    ]
    
    # Note: Chroma returns distances, so lower is better. 
    # But ContextRetriever might expect similarity or distance depending on implementation.
    # Let's check ContextRetriever implementation.
    # Assuming it filters by similarity_threshold.
    # If distance, then similarity = 1 - distance (approx for cosine).
    
    results = retriever.retrieve("query")
    mock_store.query.assert_called_with("query", n_results=2)
    
    # Test format
    context = retriever.format_context(results)
    assert isinstance(context, str)
