import os
import sys
import time
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

def run_tests():
    print("Initializing Robust Tests...")
    
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
    
    # Ensure we use the correct model
    llm_config = LLMConfig(model_name="gemma:2b") 
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
    
    test_queries = [
        {
            "name": "Filtering",
            "query": "Show me visits where the length of stay is greater than 10 days."
        },
        {
            "name": "Aggregation",
            "query": "What is the average total charge amount by payer grouping?"
        },
        {
            "name": "Sorting/Limit",
            "query": "List the top 3 visits with the highest total amount due."
        },
        {
            "name": "Complex Logic",
            "query": "Count the number of readmissions (readmit_flag = 1)."
        }
    ]
    
    for test in test_queries:
        print(f"\n{'='*50}")
        print(f"Test: {test['name']}")
        print(f"Query: {test['query']}")
        print(f"{'='*50}")
        
        try:
            start_time = time.time()
            result = orchestrator.process_query(test['query'])
            duration = time.time() - start_time
            
            print(f"Duration: {duration:.2f}s")
            print(f"Generated SQL: {result.get('generated_sql')}")
            
            if result.get("status") == "success":
                data = result["data"]
                print(f"Row Count: {data['row_count']}")
                # Print first few rows
                print("Sample Rows:")
                for i, row in enumerate(data['rows']):
                    if i >= 5:
                        print("...")
                        break
                    print(row)
            else:
                print(f"Error: {result.get('error')}")
                
        except Exception as e:
            print(f"Test Failed: {e}")

if __name__ == "__main__":
    run_tests()
