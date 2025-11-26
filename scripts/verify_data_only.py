import sqlite3
import pandas as pd

def verify_data():
    db_path = "demo.db"
    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    
    try:
        # Check tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")
        
        if ('healthyR_data',) in tables:
            # Count rows
            count = pd.read_sql("SELECT COUNT(*) as count FROM healthyR_data", conn).iloc[0]['count']
            print(f"Row count in healthyR_data: {count}")
            
            # Show sample
            print("Sample data:")
            df = pd.read_sql("SELECT * FROM healthyR_data LIMIT 5", conn)
            print(df)
        else:
            print("healthyR_data table NOT found!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verify_data()
