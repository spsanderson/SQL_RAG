"""
SQL RAG Application Entry Point
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.connection_pool import ConnectionPool
from src.database.query_executor import QueryExecutor
from src.database.schema_loader import SchemaLoader

from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.llm.sql_parser import SQLParser

from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore
from src.rag.context_retriever import ContextRetriever

from src.core.orchestrator import RAGOrchestrator
from src.core.logger import setup_logging, get_logger

logger = get_logger(__name__)

from src.core.config import load_config
from src.core.exceptions import ConfigurationError, SQLRAGException

def main():
    """
    Main application loop.
    """
    setup_logging()
    logger.info("Initializing SQL RAG Application...")
    print("Initializing SQL RAG Application...")

    # Load configurations
    try:
        # Check for config file arg or default location
        config_path = "config/config.yaml" if os.path.exists("config/config.yaml") else None
        app_config = load_config(config_path)
    except ConfigurationError as e:
        logger.error(f"Startup failed: {e}")
        print(f"Startup failed: {e}")
        return
    except Exception as e:
        logger.error(f"Unexpected startup error: {e}", exc_info=True)
        print(f"Unexpected startup error: {e}")
        return

    db_config = app_config.database
    llm_config = app_config.llm
    rag_config = app_config.rag

    # Initialize Services
    logger.info("Setting up Database connection...")
    print("Setting up Database connection...")
    pool = ConnectionPool(db_config)
    query_executor = QueryExecutor(pool)
    schema_loader = SchemaLoader(pool)

    logger.info("Setting up LLM client...")
    print("Setting up LLM client...")
    llm_client = OllamaClient(llm_config)
    dialect = "SQLite" if db_config.type == "sqlite" else "T-SQL"
    prompt_builder = PromptBuilder(dialect=dialect)
    sql_parser = SQLParser()

    logger.info("Setting up RAG module...")
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

    logger.info("Initialization Complete!")
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
            logger.info(f"Processing query: {user_input}")
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
        except SQLRAGException as e:
            logger.error(f"Application error: {e}")
            print(f"Error: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            print(f"An unexpected error occurred: {str(e)}")

    print("\nGoodbye!")

if __name__ == "__main__":
    main()
