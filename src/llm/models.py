"""
LLM Models
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LLMConfig(BaseModel):
    """
    Configuration for LLM client.
    """
    base_url: str = Field("http://localhost:11434", description="Ollama API base URL")
    model_name: str = Field("gemma:2b", description="Name of the model to use")
    timeout: int = Field(45, description="Request timeout in seconds")
    temperature: float = Field(0.1, description="Generation temperature")
    max_tokens: int = Field(512, description="Maximum tokens to generate")
    top_p: float = Field(0.9, description="Top P sampling")
    retry_attempts: int = Field(3, description="Number of retry attempts")
    rate_limit_requests: int = Field(60, description="Max requests per period")
    rate_limit_period: float = Field(60.0, description="Rate limit period in seconds")

@dataclass
class LLMResponse:
    """
    Response from the LLM.
    """
    content: str
    model: str
    prompt_eval_count: Optional[int] = None
    eval_count: Optional[int] = None
    total_duration: Optional[int] = None
