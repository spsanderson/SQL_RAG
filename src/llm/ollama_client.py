"""
Ollama Client Module.

Provides a client for interacting with the Ollama API for LLM operations.
"""
import os
import shutil
import socket
import subprocess
import time
from typing import List
from urllib.parse import urlparse

import requests

from ..core.exceptions import LLMGenerationError
from ..core.rate_limiter import RateLimiter
from .models import LLMConfig, LLMResponse


class OllamaClient:
    """Client for interacting with the Ollama API."""

    def __init__(self, config: LLMConfig):
        """
        Initialize the Ollama client.

        Args:
            config: LLM configuration settings.
        """
        self.config = config
        self.rate_limiter = RateLimiter(
            max_calls=config.rate_limit_requests,
            period=config.rate_limit_period
        )

    @staticmethod
    def ensure_service_running(config: LLMConfig) -> None:
        """
        Ensure that the Ollama service is running.

        If the service is not detected, attempt to start it automatically.

        Args:
            config: LLM configuration containing the base URL.
        """
        parsed_url = urlparse(config.base_url)
        host = parsed_url.hostname or 'localhost'
        port = parsed_url.port or 11434

        # Check if port is open
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return  # Already running

        # Not running, try to start
        print("Ollama service not detected. Attempting to start...")

        executable = shutil.which("ollama")
        if not executable:
            # Fallback for Windows
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data:
                candidate = os.path.join(
                    local_app_data, "Programs", "Ollama", "ollama.exe"
                )
                if os.path.exists(candidate):
                    executable = candidate

        if not executable:
            print(
                "Warning: 'ollama' executable not found in PATH or default "
                "location. Cannot start service automatically."
            )
            return

        try:
            # Start process with platform-specific flags
            creationflags = 0
            if os.name == 'nt':
                creationflags = subprocess.CREATE_NEW_CONSOLE

            subprocess.Popen(
                [executable, "serve"],
                creationflags=creationflags
            )

            # Wait for it to be ready
            print("Waiting for Ollama to start...")
            for _ in range(20):  # Wait up to 20 seconds
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    if sock.connect_ex((host, port)) == 0:
                        print("Ollama started successfully.")
                        return
                time.sleep(1)

            print("Warning: Timed out waiting for Ollama to start.")

        except (OSError, ValueError) as e:
            print(f"Failed to start Ollama: {e}")

    def generate(self, prompt: str) -> LLMResponse:
        """
        Generate text from a prompt using the configured model.

        Args:
            prompt: The input prompt for text generation.

        Returns:
            LLMResponse containing the generated text and metadata.

        Raises:
            LLMGenerationError: If generation fails after all retry attempts.
        """
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
                response = requests.post(
                    url, json=payload, timeout=self.config.timeout
                )
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
                    raise LLMGenerationError(
                        f"Failed to generate response from Ollama after "
                        f"{self.config.retry_attempts} attempts: {e}"
                    ) from e
                time.sleep(2 ** attempt)  # Exponential backoff

        raise LLMGenerationError("Unexpected error in Ollama generation")

    def list_models(self) -> List[str]:
        """
        List available models in Ollama.

        Returns:
            List of model names available in the Ollama instance.

        Raises:
            LLMGenerationError: If the request fails.
        """
        url = f"{self.config.base_url}/api/tags"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except requests.RequestException as e:
            raise LLMGenerationError(f"Failed to list models: {e}") from e
