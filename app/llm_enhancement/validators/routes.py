"""API routes for the Intelligent Validator"""
from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import logging

try:
    from .validator import IntelligentValidator
except ImportError:
    # For testing/mock purposes if validator is not available
    class IntelligentValidator:
        def __init__(self):
            pass
        
        async def validate_terraform(self, template_files):
            return {
                "errors": [],
                "warnings": [],
                "suggestions": []
            }
            
        async def suggest_fixes(self, template_files, validation_results):
            return template_files
        
        async def check_best_practices(self, template_files):
            return {
                "score": 80,
                "structure": {"assessment": "mock"},
                "naming": {"assessment": "mock"},
                "variables": {"assessment": "mock"},
                "security": {"assessment": "mock"},
                "recommendations": ["Mock recommendation"]
            }
        
        async def check_security(self, template_files):
            return {
                "findings": [],
                "compliance": {"status": "mock"},
                "risk_score": "low",
                "recommendations": ["Mock security recommendation"]
            }

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize the validator
validator = IntelligentValidator()

# Define request and response models
class ValidateRequest(BaseModel):
    """Request model for validate_terraform endpoint"""
    template_files: Dict[str, str]
    
class SuggestFixesRequest(BaseModel):
    """Request model for suggest_fixes endpoint"""
    template_files: Dict[str, str]
    validation_results: Dict[str, Any]
    
class BestPracticesRequest(BaseModel):
    """Request model for check_best_practices endpoint"""
    template_files: Dict[str, str]
    
class SecurityCheckRequest(BaseModel):
    """Request model for check_security endpoint"""
    template_files: Dict[str, str]

class ValidationResponse(BaseModel):
    """Response model for validate_terraform endpoint"""
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    suggestions: List[Dict[str, Any]]
    
class SuggestFixesResponse(BaseModel):
    """Response model for suggest_fixes endpoint"""
    template_files: Dict[str, str]
    
class BestPracticesResponse(BaseModel):
    """Response model for check_best_practices endpoint"""
    score: int
    structure: Dict[str, Any]
    naming: Dict[str, Any]
    variables: Dict[str, Any]
    security: Dict[str, Any]
    recommendations: List[str]
    
class SecurityCheckResponse(BaseModel):
    """Response model for check_security endpoint"""
    findings: List[Dict[str, Any]]
    compliance: Dict[str, Any]
    risk_score: str
    recommendations: List[str]

@router.post("/validate", response_model=ValidationResponse, summary="Validate Terraform template")
async def validate_terraform(request: ValidateRequest):
    """
    Validate Terraform template files for errors and best practices
    
    This endpoint analyzes Terraform files and reports errors, warnings, and suggestions
    for improvement. Use this before deploying infrastructure to catch common issues.
    """
    try:
        logger.info("Validating Terraform template...")
        results = await validator.validate_terraform(request.template_files)
        return results
    except Exception as e:
        logger.error(f"Error validating Terraform template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to validate template: {str(e)}")
        
@router.post("/suggest-fixes", response_model=SuggestFixesResponse, summary="Suggest fixes for issues")
async def suggest_fixes(request: SuggestFixesRequest):
    """
    Suggest fixes for issues identified in validation
    
    This endpoint takes validation results and original template files, then 
    returns updated files with fixes for the identified issues.
    """
    try:
        logger.info("Suggesting fixes for Terraform template...")
        fixed_files = await validator.suggest_fixes(request.template_files, request.validation_results)
        return {"template_files": fixed_files}
    except Exception as e:
        logger.error(f"Error suggesting fixes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to suggest fixes: {str(e)}")
        
@router.post("/best-practices", response_model=BestPracticesResponse, summary="Check best practices")
async def check_best_practices(request: BestPracticesRequest):
    """
    Check template for best practice adherence
    
    This endpoint analyzes Terraform files for adherence to best practices, 
    providing a score and recommendations for improvement.
    """
    try:
        logger.info("Checking best practices...")
        best_practices = await validator.check_best_practices(request.template_files)
        return best_practices
    except Exception as e:
        logger.error(f"Error checking best practices: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to check best practices: {str(e)}")
        
@router.post("/security", response_model=SecurityCheckResponse, summary="Check security")
async def check_security(request: SecurityCheckRequest):
    """
    Perform a security-focused analysis of Terraform code
    
    This endpoint analyzes Terraform files specifically for security issues,
    providing findings and recommendations focused on security best practices.
    """
    try:
        logger.info("Checking security...")
        security_results = await validator.check_security(request.template_files)
        return security_results
    except Exception as e:
        logger.error(f"Error checking security: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to check security: {str(e)}") 