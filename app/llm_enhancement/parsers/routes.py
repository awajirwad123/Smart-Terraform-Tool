"""API routes for the Natural Language Parser"""
from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import logging

try:
    from .parser import NaturalLanguageParser
except ImportError:
    # For testing/mock purposes if parser is not available
    class NaturalLanguageParser:
        def __init__(self):
            pass
        
        async def parse_infrastructure_requirements(self, text):
            return {
                "provider": "mock",
                "resources": [],
                "relationships": [],
                "security": {},
                "constraints": {},
                "metadata": {"note": "This is a mock response"}
            }
        
        async def extract_context(self, text, existing_resources=None):
            return {
                "environment": "mock",
                "region": "mock-region",
                "project": "mock-project",
                "timeline": "mock",
                "integration": [],
                "objectives": [],
                "implicit_needs": []
            }

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize the parser 
parser = NaturalLanguageParser()

# Define request and response models
class ParseRequest(BaseModel):
    """Request model for parse_requirements endpoint"""
    text: str
    
class ContextRequest(BaseModel):
    """Request model for extract_context endpoint"""
    text: str
    existing_resources: Optional[Dict[str, Any]] = None

class ParseResponse(BaseModel):
    """Response model for parse_requirements endpoint"""
    provider: str
    resources: List[Dict[str, Any]]
    relationships: Optional[List[Dict[str, Any]]] = None
    security: Optional[Dict[str, Any]] = None
    constraints: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
class ContextResponse(BaseModel):
    """Response model for extract_context endpoint"""
    environment: Optional[str] = None
    region: Optional[str] = None
    project: Optional[str] = None
    timeline: Optional[str] = None
    integration: Optional[List[str]] = None
    objectives: Optional[List[str]] = None
    implicit_needs: Optional[List[str]] = None

@router.post("/parse", response_model=ParseResponse, summary="Parse infrastructure requirements")
async def parse_requirements(request: ParseRequest):
    """
    Parse infrastructure requirements from natural language text
    
    This endpoint takes a natural language description of infrastructure needs
    and returns a structured representation of the requirements.
    """
    try:
        logger.info(f"Parsing infrastructure requirements: {request.text[:50]}...")
        requirements = await parser.parse_infrastructure_requirements(request.text)
        return requirements
    except Exception as e:
        logger.error(f"Error parsing requirements: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse requirements: {str(e)}")
        
@router.post("/context", response_model=ContextResponse, summary="Extract context from request")
async def extract_context(request: ContextRequest):
    """
    Extract contextual information from a user request
    
    This endpoint analyzes a natural language request and extracts implicit
    and explicit contextual information, such as environment, region, project, etc.
    """
    try:
        logger.info(f"Extracting context from: {request.text[:50]}...")
        context = await parser.extract_context(request.text, request.existing_resources)
        return context
    except Exception as e:
        logger.error(f"Error extracting context: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to extract context: {str(e)}") 