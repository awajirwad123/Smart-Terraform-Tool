"""API routes for the Resource Optimizer"""
from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel
import logging

from .optimizer import ResourceOptimizer

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize the optimizer
optimizer = ResourceOptimizer()

# Define request and response models
class OptimizeCostRequest(BaseModel):
    """Request model for optimize_cost endpoint"""
    template_files: Dict[str, str]
    budget_constraint: Optional[float] = None

class OptimizePerformanceRequest(BaseModel):
    """Request model for optimize_performance endpoint"""
    template_files: Dict[str, str]
    performance_targets: Optional[Dict[str, Any]] = None

class SuggestArchitectureRequest(BaseModel):
    """Request model for suggest_architecture endpoint"""
    requirements: Dict[str, Any]

class RightSizeResourcesRequest(BaseModel):
    """Request model for right_size_resources endpoint"""
    template_files: Dict[str, str]
    utilization_data: Optional[Dict[str, Any]] = None

class OptimizeCostResponse(BaseModel):
    """Response model for optimize_cost endpoint"""
    current_estimated_cost: float
    optimized_estimated_cost: float
    savings_percentage: float
    recommendations: List[Dict[str, Any]]
    template_files: Dict[str, str]

class OptimizePerformanceResponse(BaseModel):
    """Response model for optimize_performance endpoint"""
    current_performance_assessment: Dict[str, Any]
    optimized_performance_assessment: Dict[str, Any]
    improvement_summary: str
    recommendations: List[Dict[str, Any]]
    template_files: Dict[str, str]

class SuggestArchitectureResponse(BaseModel):
    """Response model for suggest_architecture endpoint"""
    architecture_overview: str
    components: List[Dict[str, Any]]
    communication: str
    scalability: str
    security: str
    cost: str
    diagram: str
    terraform_example: str

class RightSizeResourcesResponse(BaseModel):
    """Response model for right_size_resources endpoint"""
    current_resources: Dict[str, Any]
    right_sized_resources: Dict[str, Any]
    efficiency_improvement: str
    recommendations: List[Dict[str, Any]]
    template_files: Dict[str, str]

@router.post("/cost", response_model=OptimizeCostResponse, summary="Optimize for cost")
async def optimize_cost(request: OptimizeCostRequest):
    """
    Optimize Terraform template for cost
    
    This endpoint analyzes Terraform template files and suggests changes
    to reduce costs without compromising essential functionality.
    Optionally specify a budget constraint for targeted optimizations.
    """
    try:
        logger.info("Optimizing Terraform template for cost...")
        results = await optimizer.optimize_cost(request.template_files, request.budget_constraint)
        return results
    except Exception as e:
        logger.error(f"Error optimizing for cost: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to optimize for cost: {str(e)}")
        
@router.post("/performance", response_model=OptimizePerformanceResponse, summary="Optimize for performance")
async def optimize_performance(request: OptimizePerformanceRequest):
    """
    Optimize Terraform template for performance
    
    This endpoint analyzes Terraform template files and suggests changes
    to improve performance. Optionally specify performance targets for
    targeted optimizations.
    """
    try:
        logger.info("Optimizing Terraform template for performance...")
        results = await optimizer.optimize_performance(request.template_files, request.performance_targets)
        return results
    except Exception as e:
        logger.error(f"Error optimizing for performance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to optimize for performance: {str(e)}")
        
@router.post("/architecture", response_model=SuggestArchitectureResponse, summary="Suggest architecture")
async def suggest_architecture(request: SuggestArchitectureRequest):
    """
    Suggest optimal architecture based on requirements
    
    This endpoint takes infrastructure requirements and suggests an
    optimal architecture, including components, communication patterns,
    and example Terraform code.
    """
    try:
        logger.info("Suggesting architecture...")
        results = await optimizer.suggest_architecture(request.requirements)
        return results
    except Exception as e:
        logger.error(f"Error suggesting architecture: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to suggest architecture: {str(e)}")
        
@router.post("/right-size", response_model=RightSizeResourcesResponse, summary="Right-size resources")
async def right_size_resources(request: RightSizeResourcesRequest):
    """
    Right-size resources based on utilization data or best practices
    
    This endpoint analyzes Terraform template files and suggests changes
    to right-size resources based on utilization data (if provided) or
    best practices.
    """
    try:
        logger.info("Right-sizing resources...")
        results = await optimizer.right_size_resources(request.template_files, request.utilization_data)
        return results
    except Exception as e:
        logger.error(f"Error right-sizing resources: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to right-size resources: {str(e)}") 