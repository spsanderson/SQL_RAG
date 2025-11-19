"""
Test Context Retriever
"""
import pytest
from unittest.mock import MagicMock
from src.rag.context_retriever import ContextRetriever
from src.rag.models import RAGConfig, Document

@pytest.fixture
def rag_config():
    return RAGConfig(persist_directory="./test_db")

def test_format_context(rag_config):
    """
    Test formatting retrieved documents into a context string.
    """
    mock_store = MagicMock()
    retriever = ContextRetriever(rag_config, mock_store)
    
    docs = [
        Document(content="users table", metadata={"type": "table"}),
        Document(content="id column", metadata={"type": "column"}),
        Document(content="general info", metadata={"type": "doc"})
    ]
    
    context = retriever.format_context(docs)
    
    assert "Table Schema: users table" in context
    assert "Column Description: id column" in context
    assert "general info" in context
