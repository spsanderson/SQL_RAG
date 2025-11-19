"""
Test Vector Store
"""
import pytest
from unittest.mock import MagicMock, patch
from src.rag.vector_store import VectorStore
from src.rag.models import RAGConfig, Document

@pytest.fixture
def rag_config():
    return RAGConfig(persist_directory="./test_db")

@pytest.fixture
def mock_embedding_service():
    service = MagicMock()
    service.embed_documents.return_value = [[0.1, 0.2]]
    service.embed_query.return_value = [0.1, 0.2]
    return service

@patch('src.rag.vector_store.chromadb.PersistentClient')
def test_add_documents(mock_client_cls, rag_config, mock_embedding_service):
    """
    Test adding documents to the vector store.
    """
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_client_cls.return_value = mock_client
    
    store = VectorStore(rag_config, mock_embedding_service)
    docs = [Document(content="test content", metadata={"type": "table"})]
    
    store.add_documents(docs)
    
    mock_collection.add.assert_called_once()
    call_args = mock_collection.add.call_args[1]
    assert call_args['documents'] == ["test content"]
    assert call_args['metadatas'] == [{"type": "table"}]
    assert call_args['embeddings'] == [[0.1, 0.2]]

@patch('src.rag.vector_store.chromadb.PersistentClient')
def test_query(mock_client_cls, rag_config, mock_embedding_service):
    """
    Test querying the vector store.
    """
    mock_client = MagicMock()
    mock_collection = MagicMock()
    
    # Mock query result structure from ChromaDB
    mock_collection.query.return_value = {
        'ids': [['doc1']],
        'documents': [['content1']],
        'metadatas': [[{'type': 'table'}]],
        'distances': [[0.1]]
    }
    
    mock_client.get_or_create_collection.return_value = mock_collection
    mock_client_cls.return_value = mock_client
    
    store = VectorStore(rag_config, mock_embedding_service)
    results = store.query("query")
    
    assert len(results) == 1
    assert results[0].content == "content1"
    assert results[0].id == "doc1"
    assert results[0].score == 0.1
