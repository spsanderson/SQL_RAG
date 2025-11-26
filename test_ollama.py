import sys
import os
sys.path.append(os.getcwd())
os.environ["DB_PASSWORD"] = "test"
from src.core.config import load_config
from src.llm.ollama_client import OllamaClient

try:
    config = load_config("config/config.yaml")
    client = OllamaClient(config.llm)
    print(f"Testing model: {config.llm.model_name}")
    response = client.generate("Hello")
    print("Success!")
    print(f"Response: {response.content}")
except Exception as e:
    print(f"Error: {e}")
