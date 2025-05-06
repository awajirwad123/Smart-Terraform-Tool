"""LLM Enhancement Layer Configuration"""
import os
from pydantic import BaseModel
from typing import Optional, Dict, Any

class LLMEnhancementConfig(BaseModel):
    """Configuration for the LLM Enhancement Layer"""
    # Azure OpenAI configuration
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_key: str = os.getenv("AZURE_OPENAI_KEY", "")
    azure_openai_version: str = os.getenv("AZURE_OPENAI_VERSION", "2023-07-01-preview")
    
    # Deployment IDs for different models
    parser_deployment_id: str = os.getenv("AZURE_OPENAI_PARSER_DEPLOYMENT_ID", "gpt-4")
    generator_deployment_id: str = os.getenv("AZURE_OPENAI_GENERATOR_DEPLOYMENT_ID", "gpt-4")
    validator_deployment_id: str = os.getenv("AZURE_OPENAI_VALIDATOR_DEPLOYMENT_ID", "gpt-4")
    optimizer_deployment_id: str = os.getenv("AZURE_OPENAI_OPTIMIZER_DEPLOYMENT_ID", "gpt-4")
    
    # Whether to use Azure OpenAI or fallback to local mock
    use_azure_openai: bool = os.getenv("USE_AZURE_OPENAI", "true").lower() == "true"
    
    # Default model parameters
    default_temperature: float = 0.1
    max_tokens: int = 4000
    timeout: int = 60

    # Pydantic v2 config approach
    model_config = {
        "extra": "ignore"
    }

# Create a singleton instance
llm_config = LLMEnhancementConfig() 