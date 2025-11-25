"""
Setup Demo Script
"""
import os
import sys
import sqlite3
import argparse
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database.models import DatabaseConfig
from src.rag.models import RAGConfig
from scripts.ingest_schema import ingest_schema

def create_sample_data(db_path: str):
    """
    Create sample tables and data in SQLite database.
    """
    print(f"Creating sample data in {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Patients (
        PatientID INTEGER PRIMARY KEY,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        DateOfBirth DATE,
        Gender TEXT,
        Email TEXT
    )
    """)
    
    # Create Visits table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Visits (
        VisitID INTEGER PRIMARY KEY,
        PatientID INTEGER,
        VisitDate DATETIME,
        Reason TEXT,
        Diagnosis TEXT,
        FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
    )
    """)
    
    # Insert sample data
    patients = [
        (1, 'John', 'Doe', '1980-01-01', 'M', 'john.doe@example.com'),
        (2, 'Jane', 'Smith', '1990-05-15', 'F', 'jane.smith@example.com'),
        (3, 'Bob', 'Johnson', '1975-11-20', 'M', 'bob.johnson@example.com')
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO Patients VALUES (?, ?, ?, ?, ?, ?)", patients)
    
    visits = [
        (1, 1, '2023-01-10 09:00:00', 'Checkup', 'Healthy'),
        (2, 1, '2023-06-15 14:30:00', 'Fever', 'Flu'),
        (3, 2, '2023-02-20 10:15:00', 'Back pain', 'Muscle strain'),
        (4, 3, '2023-03-05 11:00:00', 'Headache', 'Migraine')
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO Visits VALUES (?, ?, ?, ?, ?)", visits)
    
    conn.commit()
    conn.close()
    print("Sample data created successfully.")

def main():
    parser = argparse.ArgumentParser(description="Setup demo environment with SQLite.")
    parser.add_argument("--db-name", default="demo.db", help="SQLite database filename")
    parser.add_argument("--persist-dir", default="./data/vector_db_demo", help="Vector store persistence directory")
    
    args = parser.parse_args()
    
    # Create sample data
    create_sample_data(args.db_name)
    
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
    
    print("\nDemo setup complete!")
    print(f"To run the demo, set the following environment variables:")
    print(f"  DB_TYPE=sqlite")
    print(f"  DB_NAME={args.db_name}")
    print(f"  RAG_PERSIST_DIRECTORY={args.persist_dir}")
    print(f"Then run: python src/main.py")

if __name__ == "__main__":
    main()
