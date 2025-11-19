"""
SQL RAG Application Entry Point
"""
import os
import sys
import yaml
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.models import DatabaseConfig
from src.database.connection_pool import ConnectionPool
from src.database.query_executor import QueryExecutor
from src.database.schema_loader import SchemaLoader

from src.llm.models import LLMConfig
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.llm.sql_parser import SQLParser

from src.rag.models import RAGConfig
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore
from src.rag.context_retriever import ContextRetriever

from src.core.orchestrator import RAGOrchestrator

def load_config(path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    """
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    """
    Main application loop.
    """
    print("Initializing SQL RAG Application...")

    # Load configurations
    # In a real app, we'd merge these or load from env
    # For now, we'll use defaults or mock values if files aren't populated
    
    # Database Config
    db_config = DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 1433)),
        database=os.getenv("DB_NAME", "MedicalDB"),
        username=os.getenv("DB_USER", "sa"),
        password=os.getenv("DB_PASSWORD", "password")
    )
    
    # LLM Config
    llm_config = LLMConfig()
    
    # RAG Config
    rag_config = RAGConfig()

    # Initialize Services
    print("Setting up Database connection...")
    pool = ConnectionPool(db_config)
    query_executor = QueryExecutor(pool)
    schema_loader = SchemaLoader(pool)

    print("Setting up LLM client...")
    llm_client = OllamaClient(llm_config)
    prompt_builder = PromptBuilder()
    sql_parser = SQLParser()

    print("Setting up RAG module...")
    embedding_service = EmbeddingService(rag_config)
    vector_store = VectorStore(rag_config, embedding_service)
    context_retriever = ContextRetriever(rag_config, vector_store)

    # Initialize Orchestrator
    orchestrator = RAGOrchestrator(
        retriever=context_retriever,
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        sql_parser=sql_parser,
        query_executor=query_executor
    )

    print("\nInitialization Complete!")
    print("Enter your question (or 'exit' to quit):")

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if not user_input.strip():
                continue

            print("Processing...")
            result = orchestrator.process_query(user_input)
            
            print("\n--- Result ---")
            if result.get("status") == "success":
                data = result["data"]
                print(f"Row Count: {data['row_count']}")
                print(f"Columns: {data['columns']}")
                print("Rows:")
                for row in data['rows']:
                    print(row)
            elif result.get("status") == "no_sql_generated":
                print("Could not generate a SQL query for this question.")
            else:
                print(f"Error: {result.get('error')}")
            
            print(f"\nGenerated SQL: {result.get('generated_sql')}")
            print("\nSteps:")
            for step in result["steps"]:
                print(f"- {step['name']}: {step['duration']:.2f}s")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    print("\nGoodbye!")

if __name__ == "__main__":
    main()
