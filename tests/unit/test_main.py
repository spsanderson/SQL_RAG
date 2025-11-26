"""
Unit tests for main.py.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.main import main

@patch("src.main.setup_logging")
@patch("src.main.load_config")
@patch("src.main.ConnectionPool")
@patch("src.main.QueryExecutor")
@patch("src.main.SchemaLoader")
@patch("src.main.OllamaClient")
@patch("src.main.PromptBuilder")
@patch("src.main.SQLParser")
@patch("src.main.EmbeddingService")
@patch("src.main.VectorStore")
@patch("src.main.ContextRetriever")
@patch("src.main.RAGOrchestrator")
@patch("builtins.input")
@patch("builtins.print")
def test_main(mock_print, mock_input, mock_orchestrator, mock_retriever, mock_vector_store, 
              mock_embedding, mock_parser, mock_prompt, mock_ollama, mock_schema, 
              mock_executor, mock_pool, mock_load_config, mock_setup_logging):
    
    # Setup mocks
    mock_input.side_effect = ["test query", "exit"]
    
    mock_orchestrator_instance = mock_orchestrator.return_value
    mock_orchestrator_instance.process_query.return_value = {
        "status": "success",
        "data": {"row_count": 1, "columns": ["id"], "rows": [{"id": 1}]},
        "generated_sql": "SELECT 1",
        "steps": [{"name": "test", "duration": 0.1}]
    }
    
    # Run main
    main()
    
    # Verify
    mock_load_config.assert_called_once()
    mock_orchestrator.assert_called_once()
    mock_orchestrator_instance.process_query.assert_called_with("test query")

@patch("src.main.setup_logging")
@patch("src.main.load_config")
@patch("builtins.print")
def test_main_config_error(mock_print, mock_load_config, mock_setup_logging):
    mock_load_config.side_effect = Exception("Config Error")
    
    main()
    
    mock_print.assert_any_call("Startup failed: Config Error")
