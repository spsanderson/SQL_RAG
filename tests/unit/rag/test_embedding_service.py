"""
Test Embedding Service
"""
import pytest
from unittest.mock import MagicMock, patch
from src.rag.embedding_service import EmbeddingService
from src.rag.models import RAGConfig

@pytest.fixture
def rag_config():
    return RAGConfig(persist_directory="./test_db")

@patch('src.rag.embedding_service.SentenceTransformer')
def test_embed_query(mock_transformer_cls, rag_config):
    """
    Test embedding a single query.
    """
    mock_model = MagicMock()
    mock_model.encode.return_value = [0.1, 0.2, 0.3] # Mock numpy array
    # We need to mock the return value of encode to be a list of numpy arrays or similar
    # The service calls tolist() on the result.
    
    # Let's mock the behavior more precisely
    import numpy as np
    mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])
    
    mock_transformer_cls.return_value = mock_model
    
    service = EmbeddingService(rag_config)
    embedding = service.embed_query("test query")
    
    assert embedding == [0.1, 0.2, 0.3]
    mock_model.encode.assert_called_once()

@patch('src.rag.embedding_service.SentenceTransformer')
def test_embed_documents(mock_transformer_cls, rag_config):
    """
    Test embedding multiple documents.
    """
    mock_model = MagicMock()
    import numpy as np
    mock_model.encode.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])
    
    mock_transformer_cls.return_value = mock_model
    
    service = EmbeddingService(rag_config)
    embeddings = service.embed_documents(["doc1", "doc2"])
    
    assert embeddings == [[0.1, 0.2], [0.3, 0.4]]
    mock_model.encode.assert_called_once()
