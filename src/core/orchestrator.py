"""
RAG Orchestrator Module.

Coordinates the RAG pipeline: context retrieval, SQL generation,
validation, and execution.
"""
import time
from typing import Any, Dict, List, Optional

from ..database.query_executor import QueryExecutor
from ..llm.ollama_client import OllamaClient
from ..llm.prompt_builder import PromptBuilder
from ..llm.sql_parser import SQLParser
from ..rag.context_retriever import ContextRetriever
from ..validation import SQLValidator
from .exceptions import DatabaseError, LLMGenerationError, SecurityError
from .logger import get_logger

logger = get_logger(__name__)


class RAGOrchestrator:
    """Orchestrates the RAG flow: Retrieve -> Generate -> Execute."""

    def __init__(
        self,
        retriever: ContextRetriever,
        llm_client: OllamaClient,
        prompt_builder: PromptBuilder,
        sql_parser: SQLParser,
        query_executor: QueryExecutor
    ):
        """
        Initialize the orchestrator.

        Args:
            retriever: Context retriever for RAG operations.
            llm_client: Client for LLM interactions.
            prompt_builder: Builds prompts for the LLM.
            sql_parser: Parses SQL from LLM responses.
            query_executor: Executes validated SQL queries.
        """
        self.retriever = retriever
        self.llm_client = llm_client
        self.prompt_builder = prompt_builder
        self.sql_parser = sql_parser
        self.query_executor = query_executor

        # Load schema for validation
        schema = self.query_executor.pool.get_adapter().get_schema()
        self.validator = SQLValidator(schema)

    def process_query(
        self,
        user_question: str,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user question and return the results.

        Args:
            user_question: The user's natural language question.
            history: Optional list of chat history messages.

        Returns:
            Dictionary containing the result with status, data, SQL,
            and processing steps.
        """
        start_time = time.time()
        result: Dict[str, Any] = {
            "question": user_question,
            "steps": []
        }

        # 1. Retrieve Context
        context_str = self._retrieve_context(user_question, result)

        # 2. Build Prompt
        prompt = self.prompt_builder.build_prompt(
            user_question=user_question,
            context_str=context_str,
            history=history
        )

        # 3. Generate and Validate SQL
        sql_query = self._generate_sql(prompt, result)
        if result.get("status") == "error":
            return result

        # 4. Execute SQL
        self._execute_sql(sql_query, result)

        result["total_duration"] = time.time() - start_time
        return result

    def _retrieve_context(
        self,
        user_question: str,
        result: Dict[str, Any]
    ) -> str:
        """Retrieve relevant context for the question."""
        retrieval_start = time.time()
        documents = self.retriever.retrieve(user_question)
        context_str = self.retriever.format_context(documents)
        result["steps"].append({
            "name": "retrieval",
            "duration": time.time() - retrieval_start,
            "documents_count": len(documents)
        })
        return context_str

    def _generate_sql(
        self,
        prompt: str,
        result: Dict[str, Any]
    ) -> str:
        """Generate and validate SQL with retry logic."""
        max_retries = 3
        current_try = 0
        last_error: Optional[str] = None
        sql_query = "NO_SQL"

        while current_try < max_retries:
            current_try += 1
            logger.info("Generation attempt %d/%d", current_try, max_retries)

            current_prompt = prompt
            if last_error:
                current_prompt += (
                    f"\n\nPrevious attempt failed with error: {last_error}\n"
                    "Please correct the query."
                )

            generation_start = time.time()
            try:
                llm_response = self.llm_client.generate(current_prompt)
                result["steps"].append({
                    "name": f"generation_try_{current_try}",
                    "duration": time.time() - generation_start,
                    "model": llm_response.model
                })

                sql_query = self.sql_parser.parse(llm_response.content)
                result["generated_sql"] = sql_query
                logger.info("Generated SQL: %s", sql_query)

                if sql_query.upper() == "NO_SQL":
                    break

                # Validate SQL
                self._validate_sql(sql_query)
                break  # Validation passed

            except SecurityError as e:
                logger.warning(
                    "SQL Validation failed on attempt %d: %s",
                    current_try, e
                )
                last_error = str(e)
                if current_try == max_retries:
                    result["status"] = "error"
                    result["error"] = (
                        f"Security Violation after {max_retries} attempts: {e}"
                    )
                    return "NO_SQL"

            except LLMGenerationError as e:
                logger.warning(
                    "Generation failed on attempt %d: %s",
                    current_try, e
                )
                last_error = str(e)
                if current_try == max_retries:
                    result["status"] = "error"
                    result["error"] = f"Generation failed: {e}"
                    return "NO_SQL"

            except Exception as e:
                logger.error(
                    "Unexpected error on attempt %d: %s",
                    current_try, e, exc_info=True
                )
                last_error = str(e)
                if current_try == max_retries:
                    result["status"] = "error"
                    result["error"] = f"Unexpected error: {e}"
                    return "NO_SQL"

        return sql_query

    def _validate_sql(self, sql_query: str) -> None:
        """Validate SQL query against security rules and schema."""
        self.validator.validate_query(sql_query)
        self.validator.validate_schema(sql_query)
        self.validator.validate_complexity(sql_query)
        self.validator.enforce_result_limit(sql_query)

    def _execute_sql(self, sql_query: str, result: Dict[str, Any]) -> None:
        """Execute the SQL query and populate the result."""
        if sql_query.upper() == "NO_SQL":
            result["status"] = "no_sql_generated"
            result["data"] = None
            return

        execution_start = time.time()
        try:
            query_result = self.query_executor.execute(sql_query)
            result["status"] = "success"
            result["data"] = {
                "columns": query_result.columns,
                "rows": query_result.rows,
                "row_count": query_result.row_count
            }
            result["steps"].append({
                "name": "execution",
                "duration": time.time() - execution_start
            })
        except DatabaseError as e:
            logger.error("Query execution failed: %s", e)
            result["status"] = "error"
            result["error"] = str(e)
            result["steps"].append({
                "name": "execution",
                "duration": time.time() - execution_start,
                "error": str(e)
            })
        except Exception as e:
            logger.error(
                "Unexpected execution error: %s", e, exc_info=True
            )
            result["status"] = "error"
            result["error"] = str(e)
            result["steps"].append({
                "name": "execution",
                "duration": time.time() - execution_start,
                "error": str(e)
            })
