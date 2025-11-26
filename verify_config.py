import os
from src.core.config import load_config

# Mock environment for SQLite without password
os.environ["DB_TYPE"] = "sqlite"
os.environ["DB_PASSWORD"] = ""
os.environ["DB_NAME"] = ":memory:"

try:
    config = load_config()
    print("Successfully loaded config for SQLite without password.")
except Exception as e:
    print(f"Failed to load config: {e}")
