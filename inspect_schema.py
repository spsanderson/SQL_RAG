import sqlite3
import json

def get_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    schema = {}
    
    # Get tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        table_info = []
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        for col in columns:
            table_info.append({
                "cid": col[0],
                "name": col[1],
                "type": col[2],
                "notnull": col[3],
                "dflt_value": col[4],
                "pk": col[5]
            })
            
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        fks = []
        for fk in cursor.fetchall():
            fks.append({
                "id": fk[0],
                "seq": fk[1],
                "table": fk[2],
                "from": fk[3],
                "to": fk[4],
                "on_update": fk[5],
                "on_delete": fk[6],
                "match": fk[7]
            })
            
        schema[table] = {
            "columns": table_info,
            "foreign_keys": fks
        }
        
    conn.close()
    return schema

if __name__ == "__main__":
    with open("schema.json", "w") as f:
        json.dump(get_schema("demo.db"), f, indent=2)
    print("Schema written to schema.json")
