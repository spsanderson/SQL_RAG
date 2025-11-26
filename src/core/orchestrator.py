"""
RAG Orchestrator
"""
import time
from typing import Dict, Any, Optional, List
from ..database.query_executor import QueryExecutor
from ..llm.ollama_client import OllamaClient
from ..llm.prompt_builder import PromptBuilder
from ..llm.sql_parser import SQLParser
from ..rag.context_retriever import ContextRetriever
from ..validation import SQLValidator
from .logger import get_logger
from .exceptions import SecurityError, LLMGenerationError, DatabaseError

logger = get_logger(__name__)

class RAGOrchestrator:
    """
    Orchestrates the RAG flow: Retrieve -> Generate -> Execute.
    """

    def __init__(
        self,
        retriever: ContextRetriever,
        llm_client: OllamaClient,
        prompt_builder: PromptBuilder,
        sql_parser: SQLParser,
        query_executor: QueryExecutor
    ):
        self.retriever = retriever
        self.llm_client = llm_client
        self.prompt_builder = prompt_builder
        self.sql_parser = sql_parser
        self.query_executor = query_executor


        # Load schema for validation
        schema = self.query_executor.pool.get_adapter().get_schema()
        self.validator = SQLValidator(schema)

    def process_query(self, user_question: str, history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Process a user question and return the results.

        Args:
            user_question: The user's question.
            history: Optional list of chat history messages.
        """
        start_time = time.time()
        result = {
            "question": user_question,
            "steps": []
        }

        # 1. Retrieve Context
        retrieval_start = time.time()
        documents = self.retriever.retrieve(user_question)
        context_str = self.retriever.format_context(documents)
        result["steps"].append({
            "name": "retrieval",
            "duration": time.time() - retrieval_start,
            "documents_count": len(documents)
        })

        # 2. Build Prompt
        prompt = self.prompt_builder.build_prompt(
            user_question=user_question,
            context_str=context_str,
            history=history
        )

        # 3. Generate SQL with Retry
        max_retries = 3
        current_try = 0
        last_error = None
        sql_query = "NO_SQL"

        while current_try < max_retries:
            current_try += 1
            logger.info(f"Generation attempt {current_try}/{max_retries}")

            # Add error context if retrying
            current_prompt = prompt
            if last_error:
                current_prompt += f"\n\nPrevious attempt failed with error: {last_error}\nPlease correct the query."

            generation_start = time.time()
            try:
                llm_response = self.llm_client.generate(current_prompt)
                result["steps"].append({
                    "name": f"generation_try_{current_try}",
                    "duration": time.time() - generation_start,
                    "model": llm_response.model
                })

                # 4. Parse SQL
                sql_query = self.sql_parser.parse(llm_response.content)
                result["generated_sql"] = sql_query
                logger.info(f"Generated SQL: {sql_query}")

                if sql_query.upper() == "NO_SQL":
                    break

                # Validate SQL
                self.validator.validate_query(sql_query)
                self.validator.validate_schema(sql_query)
                self.validator.validate_complexity(sql_query)
                self.validator.enforce_result_limit(sql_query)

                # If we get here, validation passed
                break

            except SecurityError as e:
                logger.warning(f"SQL Validation failed on attempt {current_try}: {e}")
                last_error = str(e)
                if current_try == max_retries:
                    result["status"] = "error"
                    result["error"] = f"Security Violation after {max_retries} attempts: {str(e)}"
                    return result
            except LLMGenerationError as e:
                logger.warning(f"Generation failed on attempt {current_try}: {e}")
                last_error = str(e)
                if current_try == max_retries:
                    result["status"] = "error"
                    result["error"] = f"Generation failed: {str(e)}"
                    return result
            except Exception as e:
                logger.error(f"Unexpected error on attempt {current_try}: {e}", exc_info=True)
                last_error = str(e)
                if current_try == max_retries:
                    result["status"] = "error"
                    result["error"] = f"Unexpected error: {str(e)}"
                    return result

        # 5. Execute SQL
        if sql_query.upper() == "NO_SQL":
            result["status"] = "no_sql_generated"
            result["data"] = None
        else:
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
                logger.error(f"Query execution failed: {e}")
                result["status"] = "error"
                result["error"] = str(e)
                result["steps"].append({
                    "name": "execution",
                    "duration": time.time() - execution_start,
                    "error": str(e)
                })
            except Exception as e:
                logger.error(f"Unexpected execution error: {e}", exc_info=True)
                result["status"] = "error"
                result["error"] = str(e)
                result["steps"].append({
                    "name": "execution",
                    "duration": time.time() - execution_start,
                    "error": str(e)
                })

        result["total_duration"] = time.time() - start_time
        return result
