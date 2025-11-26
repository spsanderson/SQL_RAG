import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.models import DatabaseConfig
from src.database.connection_pool import ConnectionPool
from src.database.query_executor import QueryExecutor
from src.llm.models import LLMConfig
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.llm.sql_parser import SQLParser
from src.rag.models import RAGConfig
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore
from src.rag.context_retriever import ContextRetriever
from src.core.orchestrator import RAGOrchestrator

def verify():
    print("Initializing Verification...")
    
    # Config
    db_name = "demo.db"
    db_config = DatabaseConfig(
        host="localhost",
        port=0,
        database=db_name,
        username="",
        password="",
        type="sqlite"
    )
    
    llm_config = LLMConfig() # Defaults
    rag_config = RAGConfig(persist_directory="./data/vector_db_demo")
    
    # Services
    pool = ConnectionPool(db_config)
    query_executor = QueryExecutor(pool)
    
    llm_client = OllamaClient(llm_config)
    prompt_builder = PromptBuilder(dialect="SQLite")
    sql_parser = SQLParser()
    
    embedding_service = EmbeddingService(rag_config)
    vector_store = VectorStore(rag_config, embedding_service)
    context_retriever = ContextRetriever(rag_config, vector_store)
    
    orchestrator = RAGOrchestrator(
        retriever=context_retriever,
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        sql_parser=sql_parser,
        query_executor=query_executor
    )
    
    query = "How many rows are in the healthyR_data table?"
    print(f"\nQuery: {query}")
    
    result = orchestrator.process_query(query)
    
    print("\n--- Result ---")
    if result.get("status") == "success":
        data = result["data"]
        print(f"Row Count: {data['row_count']}")
        print(f"Columns: {data['columns']}")
        print("Rows:")
        for row in data['rows']:
            print(row)
    else:
        print(f"Error: {result.get('error')}")
        print(f"Status: {result.get('status')}")

    print(f"\nGenerated SQL: {result.get('generated_sql')}")

if __name__ == "__main__":
    verify()
