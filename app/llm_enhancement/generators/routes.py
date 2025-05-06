"""API routes for the Template Generator"""
from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import logging

try:
    from .generator import TemplateGenerator
except ImportError:
    # For testing/mock purposes if generator is not available
    class TemplateGenerator:
        def __init__(self):
            pass
        
        async def generate_terraform_template(self, requirements):
            return {
                "main.tf": "# Mock Terraform code\nprovider \"aws\" {\n  region = \"us-west-2\"\n}",
                "variables.tf": "# Mock variables file",
                "outputs.tf": "# Mock outputs file"
            }
            
        async def analyze_template(self, template_files):
            return {
                "resources": [],
                "variables": [],
                "outputs": [],
                "complexity": {"level": "mock"},
                "cost": {"estimated": "mock"},
                "security": {"level": "mock"}
            }
        
        async def generate_documentation(self, template_files, analysis):
            return "# Mock Documentation\n\nThis is a mock documentation."
        
        async def customize_template(self, template_files, customizations):
            return template_files

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize the generator
generator = TemplateGenerator()

# Define request and response models
class GenerateTemplateRequest(BaseModel):
    """Request model for generate_terraform_template endpoint"""
    requirements: Dict[str, Any]

class AnalyzeTemplateRequest(BaseModel):
    """Request model for analyze_template endpoint"""
    template_files: Dict[str, str]

class GenerateDocumentationRequest(BaseModel):
    """Request model for generate_documentation endpoint"""
    template_files: Dict[str, str]
    analysis: Optional[Dict[str, Any]] = None

class CustomizeTemplateRequest(BaseModel):
    """Request model for customize_template endpoint"""
    template_files: Dict[str, str]
    customizations: Dict[str, Any]

class GenerateTemplateResponse(BaseModel):
    """Response model for generate_terraform_template endpoint"""
    template_files: Dict[str, str]

class AnalyzeTemplateResponse(BaseModel):
    """Response model for analyze_template endpoint"""
    resources: List[Dict[str, Any]]
    variables: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    complexity: Dict[str, Any]
    cost: Dict[str, Any]
    security: Dict[str, Any]

class GenerateDocumentationResponse(BaseModel):
    """Response model for generate_documentation endpoint"""
    documentation: str

class CustomizeTemplateResponse(BaseModel):
    """Response model for customize_template endpoint"""
    template_files: Dict[str, str]

@router.post("/terraform", response_model=GenerateTemplateResponse, summary="Generate Terraform template")
async def generate_terraform(request: GenerateTemplateRequest):
    """
    Generate Terraform template code based on requirements
    
    This endpoint takes structured infrastructure requirements and returns
    a set of Terraform files implementing those requirements.
    """
    try:
        logger.info("Generating Terraform template...")
        template_files = await generator.generate_terraform_template(request.requirements)
        return {"template_files": template_files}
    except Exception as e:
        logger.error(f"Error generating Terraform template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate template: {str(e)}")
        
@router.post("/analyze", response_model=AnalyzeTemplateResponse, summary="Analyze Terraform template")
async def analyze_template(request: AnalyzeTemplateRequest):
    """
    Analyze a Terraform template to extract key information
    
    This endpoint examines Terraform template files and returns structured
    information about resources, variables, outputs, complexity, cost, etc.
    """
    try:
        logger.info("Analyzing Terraform template...")
        analysis = await generator.analyze_template(request.template_files)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing Terraform template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze template: {str(e)}")
        
@router.post("/documentation", response_model=GenerateDocumentationResponse, summary="Generate documentation")
async def generate_documentation(request: GenerateDocumentationRequest):
    """
    Generate comprehensive documentation for a Terraform template
    
    This endpoint creates Markdown documentation for a Terraform template,
    including overview, usage instructions, and other key information.
    """
    try:
        logger.info("Generating documentation...")
        
        # If analysis is not provided, generate it
        analysis = request.analysis
        if not analysis:
            logger.info("No analysis provided, generating one...")
            analysis = await generator.analyze_template(request.template_files)
            
        documentation = await generator.generate_documentation(request.template_files, analysis)
        return {"documentation": documentation}
    except Exception as e:
        logger.error(f"Error generating documentation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate documentation: {str(e)}")
        
@router.post("/customize", response_model=CustomizeTemplateResponse, summary="Customize template")
async def customize_template(request: CustomizeTemplateRequest):
    """
    Customize an existing Terraform template
    
    This endpoint modifies existing Terraform template files according to
    provided customization requirements.
    """
    try:
        logger.info("Customizing Terraform template...")
        customized_files = await generator.customize_template(request.template_files, request.customizations)
        return {"template_files": customized_files}
    except Exception as e:
        logger.error(f"Error customizing template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to customize template: {str(e)}") 