"""
Integration tests for the full RAG flow.
"""
import pytest
from unittest.mock import MagicMock
from sqlalchemy import text
from src.core.orchestrator import RAGOrchestrator
from src.database.connection_pool import ConnectionPool
from src.database.query_executor import QueryExecutor
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.llm.sql_parser import SQLParser
from src.rag.context_retriever import ContextRetriever
from src.database.models import DatabaseConfig
from src.llm.models import LLMConfig, LLMResponse

@pytest.fixture
def mock_llm_client():
    client = MagicMock(spec=OllamaClient)
    return client

@pytest.fixture
def mock_retriever():
    retriever = MagicMock(spec=ContextRetriever)
    retriever.retrieve.return_value = []
    retriever.format_context.return_value = ""
    return retriever

@pytest.fixture
def db_config():
    return DatabaseConfig(
        host="localhost",
        database=":memory:",
        username="sa",
        password="password",
        type="sqlite"
    )

@pytest.fixture
def orchestrator(db_config, mock_llm_client, mock_retriever):
    pool = ConnectionPool(db_config)
    
    # Initialize DB with some data
    adapter = pool.get_adapter()
    engine = adapter.connect()
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE patients (id INTEGER PRIMARY KEY, name TEXT)"))
        conn.execute(text("INSERT INTO patients (id, name) VALUES (1, 'John Doe')"))
        conn.commit()
        
    query_executor = QueryExecutor(pool)
    prompt_builder = PromptBuilder(dialect="SQLite")
    sql_parser = SQLParser()
    
    return RAGOrchestrator(
        retriever=mock_retriever,
        llm_client=mock_llm_client,
        prompt_builder=prompt_builder,
        sql_parser=sql_parser,
        query_executor=query_executor
    )

def test_full_flow_success(orchestrator, mock_llm_client):
    # Mock LLM response
    mock_llm_client.generate.return_value = LLMResponse(
        content="SELECT * FROM patients LIMIT 10",
        model="test-model"
    )
    
    result = orchestrator.process_query("Show me all patients")
    
    assert result["status"] == "success"
    assert len(result["data"]["rows"]) == 1
    assert result["data"]["rows"][0]["name"] == "John Doe"
    assert result["generated_sql"] == "SELECT * FROM patients LIMIT 10"

def test_full_flow_validation_error_retry(orchestrator, mock_llm_client):
    # Mock LLM response: first invalid, then valid
    mock_llm_client.generate.side_effect = [
        LLMResponse(content="DROP TABLE patients", model="test-model"),
        LLMResponse(content="SELECT * FROM patients LIMIT 10", model="test-model")
    ]
    
    result = orchestrator.process_query("Delete patients")
    
    assert result["status"] == "success"
    assert len(result["data"]["rows"]) == 1
    # Verify retry happened
    assert mock_llm_client.generate.call_count == 2

def test_full_flow_no_sql(orchestrator, mock_llm_client):
    mock_llm_client.generate.return_value = LLMResponse(
        content="NO_SQL",
        model="test-model"
    )
    
    result = orchestrator.process_query("Hello")
    
    assert result["status"] == "no_sql_generated"
    assert result["data"] is None
