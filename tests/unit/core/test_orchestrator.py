"""
Test RAG Orchestrator
"""
import pytest
from unittest.mock import MagicMock, patch
from src.core.orchestrator import RAGOrchestrator
from src.llm.models import LLMResponse
from src.database.models import QueryResult

@pytest.fixture
def orchestrator_mocks():
    return {
        "retriever": MagicMock(),
        "llm_client": MagicMock(),
        "prompt_builder": MagicMock(),
        "sql_parser": MagicMock(),
        "query_executor": MagicMock()
    }

@pytest.fixture
def orchestrator(orchestrator_mocks):
    with patch('src.core.orchestrator.SQLValidator') as MockValidator:
        # Configure mock validator instance
        mock_validator_instance = MockValidator.return_value
        mock_validator_instance.validate_query.return_value = True
        mock_validator_instance.validate_schema.return_value = True
        mock_validator_instance.validate_complexity.return_value = True
        mock_validator_instance.enforce_result_limit.return_value = True
        
        yield RAGOrchestrator(**orchestrator_mocks)

def test_process_query_success(orchestrator, orchestrator_mocks):
    """
    Test successful query processing flow.
    """
    # Mock dependencies
    orchestrator_mocks["retriever"].retrieve.return_value = []
    orchestrator_mocks["retriever"].format_context.return_value = "context"
    orchestrator_mocks["prompt_builder"].build_prompt.return_value = "prompt"
    orchestrator_mocks["llm_client"].generate.return_value = LLMResponse(content="SELECT *", model="test")
    orchestrator_mocks["sql_parser"].parse.return_value = "SELECT *"
    orchestrator_mocks["query_executor"].execute.return_value = QueryResult(
        columns=["id"], rows=[{"id": 1}], row_count=1, execution_time=0.1
    )

    result = orchestrator.process_query("test question")

    assert result["status"] == "success"
    assert result["generated_sql"] == "SELECT *"
    assert result["data"]["row_count"] == 1
    
    # Verify calls
    orchestrator_mocks["retriever"].retrieve.assert_called_once()
    orchestrator_mocks["llm_client"].generate.assert_called_once()
    orchestrator_mocks["query_executor"].execute.assert_called_once()

def test_process_query_no_sql(orchestrator, orchestrator_mocks):
    """
    Test flow when no SQL is generated.
    """
    orchestrator_mocks["retriever"].retrieve.return_value = []
    orchestrator_mocks["retriever"].format_context.return_value = ""
    orchestrator_mocks["prompt_builder"].build_prompt.return_value = "prompt"
    orchestrator_mocks["llm_client"].generate.return_value = LLMResponse(content="NO_SQL", model="test")
    orchestrator_mocks["sql_parser"].parse.return_value = "NO_SQL"

    result = orchestrator.process_query("test question")

    assert result["status"] == "no_sql_generated"
    assert result["data"] is None
    orchestrator_mocks["query_executor"].execute.assert_not_called()

def test_process_query_execution_error(orchestrator, orchestrator_mocks):
    """
    Test flow when query execution fails.
    """
    orchestrator_mocks["retriever"].retrieve.return_value = []
    orchestrator_mocks["retriever"].format_context.return_value = ""
    orchestrator_mocks["prompt_builder"].build_prompt.return_value = "prompt"
    orchestrator_mocks["llm_client"].generate.return_value = LLMResponse(content="SELECT *", model="test")
    orchestrator_mocks["sql_parser"].parse.return_value = "SELECT *"
    orchestrator_mocks["query_executor"].execute.side_effect = Exception("DB Error")

    result = orchestrator.process_query("test question")

    assert result["status"] == "error"
    assert "DB Error" in result["error"]
