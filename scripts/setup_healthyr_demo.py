import rdata
import pandas as pd
import sqlite3
import os
import sys
import argparse
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.models import DatabaseConfig
from src.rag.models import RAGConfig
from scripts.ingest_schema import ingest_schema

def ingest_healthyr_data(db_path: str, rda_path: str):
    """
    Ingest healthyR data into SQLite database.
    """
    print(f"Loading data from {rda_path}...")
    if not os.path.exists(rda_path):
        print(f"Error: File not found: {rda_path}")
        return

    parsed = rdata.parser.parse_file(rda_path)
    converted = rdata.conversion.convert(parsed)
    
    # Assuming the main dataframe is the first one or named 'healthyR_data'
    # Based on inspection, it seems to be the only one or named 'healthyR_data'
    df_name = list(converted.keys())[0]
    df = converted[df_name]
    
    print(f"Found dataframe '{df_name}' with shape {df.shape}")
    
    # Clean up column names (replace . with _)
    df.columns = [c.replace('.', '_') for c in df.columns]
    
    # Convert dates if necessary (pandas usually handles this for sqlite)
    # Ensure boolean columns are handled (sqlite doesn't have native boolean, uses 0/1)
    for col in df.select_dtypes(include=['bool']).columns:
        # Convert to float first to handle NaNs, then fill with 0 (False) or keep as float/int
        # Here we fill NA with 0 for simplicity in this demo
        df[col] = df[col].fillna(False).astype(int)
        
    print(f"Connecting to database {db_path}...")
    conn = sqlite3.connect(db_path)
    
    print(f"Writing table '{df_name}'...")
    df.to_sql(df_name, conn, if_exists='replace', index=False)
    
    conn.close()
    print("Data ingestion complete.")

def main():
    parser = argparse.ArgumentParser(description="Setup demo environment with healthyR data.")
    parser.add_argument("--db-name", default="demo.db", help="SQLite database filename")
    parser.add_argument("--rda-path", default="data/healthyR_data.rda", help="Path to .rda file")
    parser.add_argument("--persist-dir", default="./data/vector_db_demo", help="Vector store persistence directory")
    
    args = parser.parse_args()
    
    # Ingest data
    ingest_healthyr_data(args.db_name, args.rda_path)
    
    # Ingest schema
    print("\nIngesting schema into RAG system...")
    
    # Set environment variables for ingestion script
    os.environ["DB_TYPE"] = "sqlite"
    os.environ["DB_NAME"] = args.db_name
    
    db_config = DatabaseConfig(
        host="localhost",
        port=0,
        database=args.db_name,
        username="",
        password="",
        type="sqlite"
    )
    
    rag_config = RAGConfig(persist_directory=args.persist_dir)
    
    ingest_schema(db_config, rag_config)
    
    print("\nSetup complete!")
    print(f"To run the demo, set the following environment variables:")
    print(f"  DB_TYPE=sqlite")
    print(f"  DB_NAME={args.db_name}")
    print(f"  RAG_PERSIST_DIRECTORY={args.persist_dir}")
    print(f"Then run: python src/main.py")

if __name__ == "__main__":
    main()
