"""
Test Ingestion Script
"""
import pytest
from unittest.mock import MagicMock, patch
from scripts.ingest_schema import ingest_schema
from src.database.models import DatabaseConfig, SchemaElement
from src.rag.models import RAGConfig

@patch('scripts.ingest_schema.ConnectionPool')
@patch('scripts.ingest_schema.SchemaLoader')
@patch('scripts.ingest_schema.EmbeddingService')
@patch('scripts.ingest_schema.VectorStore')
def test_ingest_schema_success(mock_vector_store_cls, mock_embedding_cls, mock_loader_cls, mock_pool_cls):
    """
    Test successful schema ingestion.
    """
    # Mock DB components
    mock_pool = MagicMock()
    mock_pool.get_adapter().validate_connection.return_value = True
    mock_pool_cls.return_value = mock_pool
    
    mock_loader = MagicMock()
    mock_loader.load_schema.return_value = [
        SchemaElement(name="table1", type="table", description="desc"),
        SchemaElement(name="col1", type="column", metadata={"table": "table1", "dtype": "int"})
    ]
    mock_loader_cls.return_value = mock_loader
    
    # Mock RAG components
    mock_vector_store = MagicMock()
    mock_vector_store_cls.return_value = mock_vector_store
    
    # Run ingestion
    db_config = DatabaseConfig(host="localhost", database="db", username="u", password="p")
    rag_config = RAGConfig(persist_directory="./test")
    
    ingest_schema(db_config, rag_config)
    
    # Verify interactions
    mock_pool.get_adapter().validate_connection.assert_called_once()
    mock_loader.load_schema.assert_called_once()
    mock_vector_store.add_documents.assert_called_once()
    
    # Check documents passed to vector store
    call_args = mock_vector_store.add_documents.call_args[0][0]
    assert len(call_args) == 2
    assert call_args[0].id == "table1"
    assert call_args[1].id == "col1"

@patch('scripts.ingest_schema.ConnectionPool')
def test_ingest_schema_connection_failure(mock_pool_cls):
    """
    Test graceful failure when DB connection fails.
    """
    mock_pool = MagicMock()
    mock_pool.get_adapter().validate_connection.return_value = False
    mock_pool_cls.return_value = mock_pool
    
    db_config = DatabaseConfig(host="localhost", database="db", username="u", password="p")
    rag_config = RAGConfig(persist_directory="./test")
    
    # Should return early without raising exception
    ingest_schema(db_config, rag_config)
    
    mock_pool.get_adapter().validate_connection.assert_called_once()
