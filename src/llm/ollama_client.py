"""
Ollama Client
"""
import time
import requests
from typing import List
from .models import LLMConfig, LLMResponse
from ..core.exceptions import LLMGenerationError
from ..core.rate_limiter import RateLimiter
import os
import shutil
import socket
import subprocess
from urllib.parse import urlparse

class OllamaClient:
    """
    Client for interacting with the Ollama API.
    """

    def __init__(self, config: LLMConfig):
        self.config = config
        self.rate_limiter = RateLimiter(
            max_calls=config.rate_limit_requests,
            period=config.rate_limit_period
        )

    @staticmethod
    def ensure_service_running(config: LLMConfig):
        """
        Ensure that the Ollama service is running.
        If not, attempt to start it.
        """
        parsed_url = urlparse(config.base_url)
        host = parsed_url.hostname or 'localhost'
        port = parsed_url.port or 11434

        # Check if port is open
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((host, port)) == 0:
                return # Already running

        # Not running, try to start
        print("Ollama service not detected. Attempting to start...")
        
        executable = shutil.which("ollama")
        if not executable:
            # Fallback for Windows
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data:
                candidate = os.path.join(local_app_data, "Programs", "Ollama", "ollama.exe")
                if os.path.exists(candidate):
                    executable = candidate
        
        if not executable:
            print("Warning: 'ollama' executable not found in PATH or default location. Cannot start service automatically.")
            return

        try:
            # Start process
            # Windows specific flags to avoid blocking and open in new window/console if needed
            creationflags = 0
            if os.name == 'nt':
                creationflags = subprocess.CREATE_NEW_CONSOLE
                
            subprocess.Popen(
                [executable, "serve"],
                creationflags=creationflags
            )
            
            # Wait for it to be ready
            print("Waiting for Ollama to start...")
            for _ in range(20): # Wait up to 20 seconds
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    if s.connect_ex((host, port)) == 0:
                        print("Ollama started successfully.")
                        return
                time.sleep(1)
            
            print("Warning: Timed out waiting for Ollama to start.")
            
        except Exception as e:
            print(f"Failed to start Ollama: {e}")

    def generate(self, prompt: str) -> LLMResponse:
        """
        Generate text from a prompt using the configured model.
        """
        # Acquire rate limit token
        if not self.rate_limiter.acquire(timeout=self.config.timeout):
            raise LLMGenerationError("Rate limit exceeded")

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
                    raise LLMGenerationError(f"Failed to generate response from Ollama after {self.config.retry_attempts} attempts: {str(e)}") from e
                time.sleep(2 ** attempt)  # Exponential backoff

        raise LLMGenerationError("Unexpected error in Ollama generation")

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
            raise LLMGenerationError(f"Failed to list models: {str(e)}") from e
