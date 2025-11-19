"""
RAG Orchestrator
"""
import time
from typing import Dict, Any, Optional
from ..database.query_executor import QueryExecutor
from ..llm.ollama_client import OllamaClient
from ..llm.prompt_builder import PromptBuilder
from ..llm.sql_parser import SQLParser
from ..rag.context_retriever import ContextRetriever

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

    def process_query(self, user_question: str) -> Dict[str, Any]:
        """
        Process a user question and return the results.
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
            context_str=context_str
        )

        # 3. Generate SQL
        generation_start = time.time()
        llm_response = self.llm_client.generate(prompt)
        result["steps"].append({
            "name": "generation",
            "duration": time.time() - generation_start,
            "model": llm_response.model
        })

        # 4. Parse SQL
        sql_query = self.sql_parser.parse(llm_response.content)
        result["generated_sql"] = sql_query

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
            except Exception as e:
                result["status"] = "error"
                result["error"] = str(e)
                result["steps"].append({
                    "name": "execution",
                    "duration": time.time() - execution_start,
                    "error": str(e)
                })

        result["total_duration"] = time.time() - start_time
        return result
