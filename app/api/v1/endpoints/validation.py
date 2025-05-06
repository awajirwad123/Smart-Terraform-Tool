from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter()

class ValidationRequest(BaseModel):
    template_id: Optional[str] = None
    template_content: Optional[Dict[str, str]] = None
    variables: Optional[Dict[str, Any]] = None
    scan_types: List[str] = ["syntax", "security", "cost", "best_practices"]

class ValidationIssue(BaseModel):
    severity: str
    type: str
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    resource: Optional[str] = None
    recommendation: Optional[str] = None

class ValidationResponse(BaseModel):
    valid: bool
    issues: List[ValidationIssue] = []
    execution_time: int
    scan_types: List[str]
    metadata: Dict[str, Any]

@router.post("/terraform", response_model=ValidationResponse)
async def validate_terraform(request: ValidationRequest):
    """
    Validate Terraform templates for syntax, security, cost, and best practices
    """
    # Mock response with validation issues
    # In a real implementation, this would run tfsec, terrascan, or other tools
    sample_issues = []
    
    if "security" in request.scan_types:
        sample_issues.append(
            ValidationIssue(
                severity="high",
                type="security",
                message="Security group allows ingress from 0.0.0.0/0",
                file="main.tf",
                line=15,
                resource="aws_security_group.allow_all",
                recommendation="Restrict ingress to specific CIDR blocks"
            )
        )
    
    if "cost" in request.scan_types:
        sample_issues.append(
            ValidationIssue(
                severity="medium",
                type="cost",
                message="Instance type m5.xlarge might be oversized",
                file="instances.tf",
                line=23,
                resource="aws_instance.application",
                recommendation="Consider using a smaller instance type or auto-scaling"
            )
        )
    
    return {
        "valid": len(sample_issues) == 0,
        "issues": sample_issues,
        "execution_time": 1250,  # milliseconds
        "scan_types": request.scan_types,
        "metadata": {
            "template_id": request.template_id,
            "files_scanned": 5,
            "resources_analyzed": 12
        }
    }

@router.post("/policy", response_model=ValidationResponse)
async def validate_against_policies(request: ValidationRequest):
    """
    Validate Terraform templates against organizational policies
    """
    # Mock response for policy validation
    # In a real implementation, this would check against OPA/Rego policies
    return {
        "valid": False,
        "issues": [
            ValidationIssue(
                severity="critical",
                type="policy",
                message="Missing required tags for compliance",
                file="main.tf",
                line=8,
                resource="aws_s3_bucket.data",
                recommendation="Add required tags: environment, owner, cost-center"
            )
        ],
        "execution_time": 850,  # milliseconds
        "scan_types": ["policy_compliance"],
        "metadata": {
            "template_id": request.template_id,
            "policies_checked": 15,
            "resources_analyzed": 12
        }
    } 