"""
SQL RAG Streamlit Application.

Provides a web-based chat interface for natural language SQL queries.
"""
import os
import sys

import pandas as pd
import streamlit as st

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.config import load_config
from src.core.logger import get_logger
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

st.set_page_config(page_title="SQL RAG Assistant", layout="wide")

# Default schema file path for the demo.
# This file should be located at the project root (same directory as demo.db).
# It contains the database schema definitions for table/column validation.
SCHEMA_JSON_PATH = "schema.json"


@st.cache_resource
def get_orchestrator():
    """
    Initialize and cache the orchestrator.

    Returns:
        RAGOrchestrator instance or None if initialization fails.
    """
    try:
        config_path = (
            "config/config.yaml"
            if os.path.exists("config/config.yaml")
            else None
        )
        app_config = load_config(config_path)

        # Initialize services
        db_pool = ConnectionPool(app_config.database)
        query_executor = QueryExecutor(db_pool)

        llm_client = OllamaClient(app_config.llm)

        embedding_service = EmbeddingService(app_config.rag)
        vector_store = VectorStore(app_config.rag, embedding_service)
        context_retriever = ContextRetriever(app_config.rag, vector_store)

        dialect = "SQLite" if app_config.database.type == "sqlite" else "T-SQL"
        prompt_builder = PromptBuilder(dialect=dialect)
        sql_parser = SQLParser()

        orchestrator = RAGOrchestrator(
            retriever=context_retriever,
            llm_client=llm_client,
            prompt_builder=prompt_builder,
            sql_parser=sql_parser,
            query_executor=query_executor
        )

        # If schema.json exists, set up additional validation
        if os.path.exists(SCHEMA_JSON_PATH):
            from src.validation.validator import SQLValidator
            orchestrator.validator = SQLValidator(
                schema_json_path=SCHEMA_JSON_PATH
            )
            logger.info("Loaded schema validation from %s", SCHEMA_JSON_PATH)

        return orchestrator

    except Exception as e:
        st.error(f"Failed to initialize application: {e}")
        logger.error("Failed to initialize application: %s", e, exc_info=True)
        return None


def display_message(message):
    """Display a chat message with optional data and SQL."""
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "data" in message and message["data"] is not None:
            st.dataframe(message["data"])
        if "sql" in message:
            with st.expander("Generated SQL"):
                st.code(message["sql"], language="sql")


def process_user_query(orchestrator, prompt):
    """
    Process a user query and return the response.

    Args:
        orchestrator: RAGOrchestrator instance.
        prompt: User's natural language query.

    Returns:
        Dictionary with response data.
    """
    # Build history from session state
    history = []
    for msg in st.session_state.messages:
        if msg["role"] in ("user", "assistant"):
            history.append({
                "role": msg["role"],
                "content": msg["content"]
            })

    return orchestrator.process_query(prompt, history=history)


def main():
    """Main Streamlit application entry point."""
    st.title("SQL RAG Assistant")

    orchestrator = get_orchestrator()
    if not orchestrator:
        return

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages
    for message in st.session_state.messages:
        display_message(message)

    # Handle new user input
    if prompt := st.chat_input("Ask a question about the data..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = process_user_query(orchestrator, prompt)

                    if result["status"] == "success":
                        response_text = "Here are the results:"
                        data = pd.DataFrame(result["data"]["rows"])
                        st.markdown(response_text)
                        st.dataframe(data)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text,
                            "data": data,
                            "sql": result.get("generated_sql")
                        })

                        with st.expander("Generated SQL"):
                            st.code(result.get("generated_sql"), language="sql")

                    elif result["status"] == "no_sql_generated":
                        response_text = (
                            "I couldn't generate a valid SQL query for your request."
                        )
                        st.markdown(response_text)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text
                        })

                    else:
                        response_text = f"Error: {result.get('error')}"
                        st.error(response_text)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text
                        })

                except Exception as e:
                    logger.error("Query processing error: %s", e, exc_info=True)
                    st.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
