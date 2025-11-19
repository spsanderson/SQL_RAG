"""
Ollama Client
"""
import time
import requests
from typing import Optional, Dict, Any, List
from .models import LLMConfig, LLMResponse

class OllamaClient:
    """
    Client for interacting with the Ollama API.
    """
    
    def __init__(self, config: LLMConfig):
        self.config = config

    def generate(self, prompt: str) -> LLMResponse:
        """
        Generate text from a prompt using the configured model.
        """
        url = f"{self.config.base_url}/api/generate"
        payload = {
            "model": self.config.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
                "top_p": self.config.top_p
            }
        }

        for attempt in range(self.config.retry_attempts):
            try:
                response = requests.post(url, json=payload, timeout=self.config.timeout)
                response.raise_for_status()
                data = response.json()
                
                return LLMResponse(
                    content=data.get("response", ""),
                    model=data.get("model", self.config.model_name),
                    prompt_eval_count=data.get("prompt_eval_count"),
                    eval_count=data.get("eval_count"),
                    total_duration=data.get("total_duration")
                )
            except requests.RequestException as e:
                if attempt == self.config.retry_attempts - 1:
                    raise Exception(f"Failed to generate response from Ollama after {self.config.retry_attempts} attempts: {str(e)}") from e
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("Unexpected error in Ollama generation")

    def list_models(self) -> List[str]:
        """
        List available models in Ollama.
        """
        url = f"{self.config.base_url}/api/tags"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except requests.RequestException as e:
            raise Exception(f"Failed to list models: {str(e)}") from e
