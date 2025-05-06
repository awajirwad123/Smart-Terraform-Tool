"""Natural Language Parser for infrastructure requirements"""
from typing import Dict, List, Optional, Any
import json
from ..base import LLMComponentBase

class NaturalLanguageParser(LLMComponentBase):
    """
    Natural Language Parser for extracting infrastructure requirements from text.
    
    This component handles:
    1. Infrastructure from Text: Parse natural language into structured infra requirements
    2. Requirement Extraction: Identify specific technical needs from general descriptions
    3. Context Awareness: Maintain awareness of the broader context of requests
    """
    
    def __init__(self, deployment_id: Optional[str] = None):
        """Initialize the Natural Language Parser component"""
        super().__init__("parser", deployment_id)
        
        # Register some mock responses for testing when Azure OpenAI is not available
        self._register_default_mocks()
    
    async def parse_infrastructure_requirements(self, text: str) -> Dict[str, Any]:
        """
        Parse infrastructure requirements from natural language text.
        
        Args:
            text: Natural language description of infrastructure needs
            
        Returns:
            Structured infrastructure requirements
        """
        system_prompt = """
        You are an expert infrastructure architect that specializes in extracting clear, structured 
        infrastructure requirements from natural language descriptions. Your task is to:
        
        1. Identify the cloud provider(s) mentioned or implied
        2. Extract infrastructure resources needed (VMs, networks, storage, etc.)
        3. Identify relationships between resources
        4. Extract configuration parameters mentioned
        5. Identify security and compliance requirements
        6. Note any performance or cost constraints
        
        Format your response as a structured JSON object with the following keys:
        - provider: The cloud provider (aws, azure, gcp, etc.)
        - resources: Array of resources with their types and configurations
        - relationships: How resources connect or depend on each other
        - security: Security requirements and considerations
        - constraints: Any performance or cost constraints
        - metadata: Any additional information or context
        """
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=text,
            json_response=True,
            mock_response_key="parse_requirements"
        )
            
    async def extract_context(self, text: str, existing_resources: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract context from user's request and existing resources.
        
        Args:
            text: User's natural language request
            existing_resources: Dictionary of existing resources (if available)
            
        Returns:
            Contextual information extracted
        """
        system_prompt = """
        As an infrastructure context specialist, analyze the user's request and extract contextual information.
        Consider any implicit or explicit references to:
        
        1. Development environment (dev, test, prod)
        2. Regional preferences or requirements
        3. Team or project context
        4. Time-based requirements (temporary vs permanent)
        5. Integration with existing systems
        6. Business objectives driving the request
        
        Format your response as a structured JSON object with the following keys:
        - environment: The target environment (dev, test, prod, etc.)
        - region: Geographical region or regions
        - project: Project or team context
        - timeline: Temporary or permanent, and any timing requirements
        - integration: Systems to integrate with
        - objectives: Business goals driving the request
        - implicit_needs: Requirements that weren't explicitly stated but are implied
        """
        
        user_content = text
        if existing_resources:
            user_content += f"\n\nExisting resources: {json.dumps(existing_resources)}"
        
        return await self.call_llm(
            system_prompt=system_prompt,
            user_content=user_content,
            json_response=True,
            mock_response_key="extract_context"
        )
    
    def _register_default_mocks(self):
        """Register default mock responses for testing"""
        # Mock response for parsing requirements
        self.register_mock_response("parse_requirements", {
            "provider": "aws",
            "resources": [
                {
                    "type": "vpc",
                    "name": "main-vpc",
                    "cidr": "10.0.0.0/16",
                    "subnets": [
                        {"name": "public-1", "cidr": "10.0.1.0/24", "az": "us-west-2a"},
                        {"name": "private-1", "cidr": "10.0.2.0/24", "az": "us-west-2a"}
                    ]
                },
                {
                    "type": "ec2",
                    "name": "web-server",
                    "instance_type": "t3.medium",
                    "count": 2
                }
            ],
            "relationships": [
                {"source": "web-server", "target": "public-1", "type": "deployed_in"}
            ],
            "security": {
                "encryption": "required",
                "access_controls": ["restrict_ssh_access", "use_security_groups"]
            },
            "constraints": {
                "budget": "low_cost",
                "performance": "moderate"
            },
            "metadata": {
                "purpose": "Web application hosting",
                "requestor": "Development team"
            }
        })
        
        # Mock response for extracting context
        self.register_mock_response("extract_context", {
            "environment": "dev",
            "region": "us-west-2",
            "project": "web-app-modernization",
            "timeline": "permanent",
            "integration": ["existing_database", "authentication_service"],
            "objectives": ["improve_scalability", "reduce_operational_cost"],
            "implicit_needs": ["high_availability", "auto_scaling"]
        }) 