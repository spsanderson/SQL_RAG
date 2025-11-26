"""
SQL RAG Streamlit Application
"""
import streamlit as st
import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.core.config import load_config
from src.core.orchestrator import RAGOrchestrator
from src.database.connection_pool import ConnectionPool
from src.database.query_executor import QueryExecutor
from src.llm.ollama_client import OllamaClient
from src.llm.prompt_builder import PromptBuilder
from src.llm.sql_parser import SQLParser
from src.rag.context_retriever import ContextRetriever
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore
from src.core.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="SQL RAG Assistant", layout="wide")

@st.cache_resource
def get_orchestrator():
    """
    Initialize and cache the orchestrator.
    """
    try:
        # Load config
        # We assume config file is in default location or env vars are set
        config_path = "config/config.yaml" if os.path.exists("config/config.yaml") else None
        app_config = load_config(config_path)
        
        # Initialize services
        db_pool = ConnectionPool(app_config.database)
        query_executor = QueryExecutor(db_pool)
        
        llm_client = OllamaClient(app_config.llm)
        
        embedding_service = EmbeddingService(app_config.rag)
        vector_store = VectorStore(app_config.rag, embedding_service)
        context_retriever = ContextRetriever(vector_store, app_config.rag)
        
        dialect = "SQLite" if app_config.database.type == "sqlite" else "T-SQL"
        prompt_builder = PromptBuilder(dialect=dialect)
        sql_parser = SQLParser()
        
        return RAGOrchestrator(
            retriever=context_retriever,
            llm_client=llm_client,
            prompt_builder=prompt_builder,
            sql_parser=sql_parser,
            query_executor=query_executor
        )
    except Exception as e:
        st.error(f"Failed to initialize application: {e}")
        return None

def main():
    st.title("SQL RAG Assistant")
    
    orchestrator = get_orchestrator()
    if not orchestrator:
        return

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "data" in message and message["data"] is not None:
                st.dataframe(message["data"])
            if "sql" in message:
                with st.expander("Generated SQL"):
                    st.code(message["sql"], language="sql")

    if prompt := st.chat_input("Ask a question about the data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Pass history to orchestrator
                    # Filter messages to only include user and assistant text content
                    history = []
                    for msg in st.session_state.messages:
                        if msg["role"] in ["user", "assistant"]:
                            history.append({
                                "role": msg["role"],
                                "content": msg["content"]
                            })
                            
                    result = orchestrator.process_query(prompt, history=history)
                    
                    if result["status"] == "success":
                        response_text = "Here are the results:"
                        data = pd.DataFrame(result["data"]["rows"])
                        st.markdown(response_text)
                        st.dataframe(data)
                        
                        # Add to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text,
                            "data": data,
                            "sql": result.get("generated_sql")
                        })
                        
                        with st.expander("Generated SQL"):
                            st.code(result.get("generated_sql"), language="sql")
                            
                    elif result["status"] == "no_sql_generated":
                        response_text = "I couldn't generate a valid SQL query for your request."
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
                    st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
