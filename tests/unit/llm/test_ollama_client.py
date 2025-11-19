"""
Test Ollama Client
"""
import pytest
import requests
from unittest.mock import MagicMock, patch
from src.llm.ollama_client import OllamaClient
from src.llm.models import LLMConfig

@pytest.fixture
def llm_config():
    return LLMConfig(base_url="http://mock-url")

@patch('src.llm.ollama_client.requests.post')
def test_generate_success(mock_post, llm_config):
    """
    Test successful generation.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": "SELECT * FROM users",
        "model": "sqlcoder",
        "total_duration": 100
    }
    mock_post.return_value = mock_response
    
    client = OllamaClient(llm_config)
    response = client.generate("test prompt")
    
    assert response.content == "SELECT * FROM users"
    assert response.model == "sqlcoder"
    assert response.total_duration == 100

@patch('src.llm.ollama_client.requests.post')
def test_generate_retry_logic(mock_post, llm_config):
    """
    Test that the client retries on failure.
    """
    # Fail twice, then succeed
    mock_response_success = MagicMock()
    mock_response_success.json.return_value = {"response": "success"}
    
    mock_post.side_effect = [
        requests.ConnectionError("Connection error"),
        requests.Timeout("Timeout"),
        mock_response_success
    ]
    
    client = OllamaClient(llm_config)
    response = client.generate("test prompt")
    
    assert response.content == "success"
    assert mock_post.call_count == 3
