"""
Schema Export Script
Exports the database schema to a JSON file.
"""
import os
import sys
import json
import argparse
from typing import Any
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.models import DatabaseConfig
from src.database.connection_pool import ConnectionPool
from src.database.schema_loader import SchemaLoader

def export_schema(db_config: DatabaseConfig, output_file: str):
    """
    Connects to the database, loads the schema, and writes it to a JSON file.
    """
    print(f"Connecting to database ({db_config.type})...")
    pool = ConnectionPool(db_config)
    
    try:
        if not pool.get_adapter().validate_connection():
            print("Error: Could not connect to the database.")
            return

        loader = SchemaLoader(pool)
        print("Loading schema...")
        schema_elements = loader.load_schema()
        
        # Convert schema elements to a JSON-serializable format
        export_data = []
        for element in schema_elements:
            export_data.append({
                "name": element.name,
                "type": element.type,
                "description": element.description,
                "metadata": element.metadata
            })
            
        print(f"Found {len(export_data)} schema elements.")
        
        print(f"Writing to {output_file}...")
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        print("Export complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pool.dispose()

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Export database schema to JSON.")
    parser.add_argument("--host", default=os.getenv("DB_HOST", "localhost"), help="Database host")
    parser.add_argument("--port", type=int, default=int(os.getenv("DB_PORT", 1433)), help="Database port")
    parser.add_argument("--database", default=os.getenv("DB_NAME", "MedicalDB"), help="Database name")
    parser.add_argument("--username", default=os.getenv("DB_USER", "sa"), help="Database username")
    parser.add_argument("--password", default=os.getenv("DB_PASSWORD"), help="Database password")
    parser.add_argument("--type", default=os.getenv("DB_TYPE", "sqlserver"), help="Database type")
    parser.add_argument("--output", default="schema_export.json", help="Output JSON file path")
    
    args = parser.parse_args()
    
    # Password check for non-sqlite
    if args.type != 'sqlite' and not args.password:
        print("Error: Password is required via --password or DB_PASSWORD env var for non-sqlite databases.")
        sys.exit(1)
        
    db_config = DatabaseConfig(
        host=args.host,
        port=args.port,
        database=args.database,
        username=args.username,
        password=args.password or "", # Ensure string for pydantic
        type=args.type
    )
    
    export_schema(db_config, args.output)

if __name__ == "__main__":
    main()
