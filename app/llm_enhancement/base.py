"""Base class for all LLM Enhancement components"""
import openai
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel
from .config import llm_config

# Configure logging
logger = logging.getLogger(__name__)

class MockCompletionChoice:
    """Mock completion choice for testing"""
    def __init__(self, content: str):
        self.message = type('obj', (object,), {
            'content': content,
            'function_call': None
        })

class MockCompletion:
    """Mock completion for testing"""
    def __init__(self, content: str):
        self.choices = [MockCompletionChoice(content)]

class LLMComponentBase:
    """Base class for all LLM Enhancement components"""
    
    def __init__(self, component_name: str, deployment_id: Optional[str] = None):
        """
        Initialize the LLM component.
        
        Args:
            component_name: Name of the component for logging
            deployment_id: Override the default deployment ID from config
        """
        self.component_name = component_name
        self.deployment_id = deployment_id or getattr(llm_config, f"{component_name.lower()}_deployment_id")
        self.mock_responses = {}
        
        # Initialize Azure OpenAI client if configured
        if llm_config.use_azure_openai:
            if not llm_config.azure_openai_endpoint or not llm_config.azure_openai_key:
                logger.warning(f"Azure OpenAI credentials not provided. {component_name} will use mock responses.")
            else:
                try:
                    self.client = openai.AzureOpenAI(
                        azure_endpoint=llm_config.azure_openai_endpoint,
                        api_key=llm_config.azure_openai_key,
                        api_version=llm_config.azure_openai_version
                    )
                    logger.info(f"Initialized {component_name} with Azure OpenAI deployment {self.deployment_id}")
                except Exception as e:
                    logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
                    self.client = None
        else:
            logger.info(f"{component_name} configured to use mock responses")
            self.client = None
    
    async def call_llm(self, 
                       system_prompt: str, 
                       user_content: Union[str, Dict], 
                       temperature: Optional[float] = None,
                       json_response: bool = True,
                       max_tokens: Optional[int] = None,
                       mock_response_key: Optional[str] = None) -> Any:
        """
        Make a call to the LLM with appropriate error handling.
        
        Args:
            system_prompt: System prompt for the model
            user_content: User content for the model (string or dict)
            temperature: Temperature for sampling (higher = more creative)
            json_response: Whether to expect a JSON response
            max_tokens: Maximum tokens to generate
            mock_response_key: Key to identify mock response
            
        Returns:
            Either JSON object or raw string response
        """
        # Format user content if it's a dictionary
        if isinstance(user_content, dict):
            user_content = json.dumps(user_content)
        
        # Use mock response if client not available or mock explicitly configured
        if self.client is None or not llm_config.use_azure_openai:
            return await self._get_mock_response(mock_response_key, system_prompt, user_content, json_response)
        
        try:
            # Configure response format if JSON is expected
            response_format = {"type": "json_object"} if json_response else None
            
            # Call Azure OpenAI
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.deployment_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format=response_format,
                temperature=temperature or llm_config.default_temperature,
                max_tokens=max_tokens or llm_config.max_tokens
            )
            
            # Extract content
            content = response.choices[0].message.content
            
            # Parse as JSON if requested
            if json_response:
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {str(e)}")
                    logger.debug(f"Raw response: {content}")
                    raise Exception(f"Invalid JSON response from LLM: {str(e)}")
            
            return content
            
        except Exception as e:
            logger.error(f"Error calling Azure OpenAI: {str(e)}")
            # Fallback to mock response in case of error
            return await self._get_mock_response(mock_response_key, system_prompt, user_content, json_response)
    
    async def _get_mock_response(self, 
                                 key: Optional[str], 
                                 system_prompt: str, 
                                 user_content: str,
                                 json_response: bool) -> Any:
        """Get a mock response for testing purposes"""
        if key and key in self.mock_responses:
            mock_data = self.mock_responses[key]
            logger.info(f"Using mock response for key: {key}")
            return mock_data
        
        # Generic mock response
        mock = {
            "message": f"This is a mock response from {self.component_name}",
            "system_prompt_length": len(system_prompt),
            "user_content_preview": user_content[:50] + "..." if len(user_content) > 50 else user_content
        }
        
        if json_response:
            return mock
        return json.dumps(mock)
    
    def register_mock_response(self, key: str, response: Any) -> None:
        """Register a mock response for testing"""
        self.mock_responses[key] = response
        logger.info(f"Registered mock response for key: {key}") 