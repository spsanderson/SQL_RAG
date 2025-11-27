"""
SQL RAG Application Entry Point.

Main CLI interface for the SQL RAG natural language to SQL system.
"""
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.config import load_config
from src.core.exceptions import ConfigurationError, SQLRAGException
from src.core.logger import get_logger, setup_logging
from src.core.orchestrator import RAGOrchestrator
from src.database.connection_pool import ConnectionPool
from src.database.query_executor import QueryExecutor
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.llm.sql_parser import SQLParser
from src.rag.context_retriever import ContextRetriever
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore

logger = get_logger(__name__)


def initialize_services(app_config):
    """
    Initialize all application services.

    Args:
        app_config: Application configuration object.

    Returns:
        Tuple of (orchestrator, pool) for use in main loop.
    """
    logger.info("Setting up Database connection...")
    print("Setting up Database connection...")
    pool = ConnectionPool(app_config.database)
    query_executor = QueryExecutor(pool)

    logger.info("Setting up LLM client...")
    print("Setting up LLM client...")
    OllamaClient.ensure_service_running(app_config.llm)
    llm_client = OllamaClient(app_config.llm)
    dialect = "SQLite" if app_config.database.type == "sqlite" else "T-SQL"
    prompt_builder = PromptBuilder(dialect=dialect)
    sql_parser = SQLParser()

    logger.info("Setting up RAG module...")
    print("Setting up RAG module...")
    embedding_service = EmbeddingService(app_config.rag)
    vector_store = VectorStore(app_config.rag, embedding_service)
    context_retriever = ContextRetriever(app_config.rag, vector_store)

    orchestrator = RAGOrchestrator(
        retriever=context_retriever,
        llm_client=llm_client,
        prompt_builder=prompt_builder,
        sql_parser=sql_parser,
        query_executor=query_executor
    )

    return orchestrator


def process_user_input(orchestrator, user_input: str) -> None:
    """
    Process a single user input and display results.

    Args:
        orchestrator: RAG orchestrator instance.
        user_input: User's natural language question.
    """
    print("Processing...")
    logger.info("Processing query: %s", user_input)
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


def main() -> None:
    """Main application entry point."""
    setup_logging()
    logger.info("Initializing SQL RAG Application...")
    print("Initializing SQL RAG Application...")

    # Load configurations
    try:
        config_path = (
            "config/config.yaml"
            if os.path.exists("config/config.yaml")
            else None
        )
        app_config = load_config(config_path)
    except ConfigurationError as e:
        logger.error("Startup failed: %s", e)
        print(f"Startup failed: {e}")
        return

    try:
        orchestrator = initialize_services(app_config)
    except Exception as e:
        logger.error("Failed to initialize services: %s", e, exc_info=True)
        print(f"Failed to initialize services: {e}")
        return

    logger.info("Initialization Complete!")
    print("\nInitialization Complete!")
    print("Enter your question (or 'exit' to quit):")

    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() in ('exit', 'quit'):
                break

            if not user_input.strip():
                continue

            process_user_input(orchestrator, user_input)

        except KeyboardInterrupt:
            break
        except SQLRAGException as e:
            logger.error("Application error: %s", e)
            print(f"Error: {e}")
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e, exc_info=True)
            print(f"An unexpected error occurred: {e}")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
