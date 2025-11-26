"""
Schema Ingestion Script
"""
import os
import sys
import argparse
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.models import DatabaseConfig
from src.database.connection_pool import ConnectionPool
from src.database.schema_loader import SchemaLoader
from src.rag.models import RAGConfig, Document
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore

def ingest_schema(db_config: DatabaseConfig, rag_config: RAGConfig):
    """
    Extracts schema from database and ingests into vector store.
    """
    print("Initializing services...")
    
    # Database setup
    pool = ConnectionPool(db_config)
    schema_loader = SchemaLoader(pool)
    
    # RAG setup
    embedding_service = EmbeddingService(rag_config)
    vector_store = VectorStore(rag_config, embedding_service)
    
    print("Connecting to database...")
    try:
        # Test connection
        if not pool.get_adapter().validate_connection():
            print("Error: Could not connect to the database. Please check your configuration.")
            return
            
        print("Loading schema...")
        schema_elements = schema_loader.load_schema()
        print(f"Found {len(schema_elements)} schema elements.")
        
        print("Converting to documents...")
        documents = []
        for element in schema_elements:
            # Manual descriptions overrides
            manual_descriptions = {
                "healthyR_data": "Contains detailed patient visit data including length of stay, charges, and readmission flags. Use this for analysis of hospital stays, visits, and financial data.",
                "Visits": "Basic visit log. For detailed analysis of length of stay or charges, use healthyR_data instead."
            }
            
            # Create a rich text representation for embedding
            if element.type == 'table':
                description = manual_descriptions.get(element.name, element.description or 'No description')
                content = f"Table: {element.name}\nDescription: {description}"
            elif element.type == 'column':
                content = f"Column: {element.name}\nType: {element.metadata.get('dtype')}\nTable: {element.metadata.get('table')}\nDescription: {element.description or 'No description'}"
            else:
                content = f"{element.name}: {element.description}"
            
            doc = Document(
                id=element.name,
                content=content,
                metadata={
                    "type": element.type,
                    "name": element.name,
                    ** (element.metadata or {})
                }
            )
            documents.append(doc)
            
        print(f"Ingesting {len(documents)} documents into vector store...")
        vector_store.add_documents(documents)
        
        print("Ingestion complete!")
        
    except Exception as e:
        print(f"An error occurred during ingestion: {str(e)}")
    finally:
        pool.dispose()

def main():
    parser = argparse.ArgumentParser(description="Ingest database schema into RAG vector store.")
    parser.add_argument("--host", default=os.getenv("DB_HOST", "localhost"), help="Database host")
    parser.add_argument("--port", type=int, default=int(os.getenv("DB_PORT", 1433)), help="Database port")
    parser.add_argument("--database", default=os.getenv("DB_NAME", "MedicalDB"), help="Database name")
    parser.add_argument("--username", default=os.getenv("DB_USER", "sa"), help="Database username")
    parser.add_argument("--password", default=os.getenv("DB_PASSWORD"), help="Database password")
    parser.add_argument("--persist-dir", default="./data/vector_db", help="Vector store persistence directory")
    
    parser.add_argument("--type", default=os.getenv("DB_TYPE", "sqlserver"), help="Database type")
    
    args = parser.parse_args()
    
    if not args.password:
        print("Error: Password is required via --password or DB_PASSWORD env var.")
        sys.exit(1)
    
    db_config = DatabaseConfig(
        host=args.host,
        port=args.port,
        database=args.database,
        username=args.username,
        password=args.password,
        type=args.type
    )
    
    rag_config = RAGConfig(persist_directory=args.persist_dir)
    
    ingest_schema(db_config, rag_config)

if __name__ == "__main__":
    main()
