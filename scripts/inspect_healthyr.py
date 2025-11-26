import rdata
import pandas as pd
import os

file_path = 'data/healthyR_data.rda'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

try:
    parsed = rdata.parser.parse_file(file_path)
    converted = rdata.conversion.convert(parsed)
    
    print(f"Keys found: {converted.keys()}")
    
    for key, df in converted.items():
        print(f"\n--- Dataframe: {key} ---")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Types:\n{df.dtypes}")
        print(f"Head:\n{df.head()}")
        
except Exception as e:
    print(f"Error reading file: {e}")
