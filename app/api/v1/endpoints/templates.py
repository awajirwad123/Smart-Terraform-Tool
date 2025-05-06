from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

router = APIRouter()

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    tags: List[str] = []
    provider: str
    version: str
    
class TemplateCreate(TemplateBase):
    pass

class TemplateResponse(TemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime
    created_by: str
    usage_count: int
    avg_execution_time: Optional[int] = None
    variables: List[Dict[str, Any]]

@router.post("/", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(template: TemplateCreate):
    """
    Create a new template (metadata only)
    """
    # Mock response - would actually create in DB
    template_id = "template-12345"
    now = datetime.now().isoformat()
    
    return {
        **template.dict(),
        "id": template_id,
        "created_at": now,
        "updated_at": now,
        "created_by": "user123",
        "usage_count": 0,
        "avg_execution_time": None,
        "variables": []
    }

@router.post("/upload")
async def upload_template_files(
    template_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Upload Terraform template files to an existing template
    """
    # Would validate template_id exists and process files
    # For now, just return the filenames
    return {
        "template_id": template_id,
        "uploaded_files": [file.filename for file in files]
    }

@router.get("/", response_model=List[TemplateResponse])
async def list_templates(
    provider: Optional[str] = None,
    tag: Optional[str] = None,
):
    """
    List and filter templates
    """
    # Mock response - would query from DB with filters
    now = datetime.now().isoformat()
    return [
        {
            "id": "template-12345",
            "name": "AWS VPC",
            "description": "Basic AWS VPC setup",
            "tags": ["aws", "networking", "vpc"],
            "provider": provider or "aws",
            "version": "1.0.0",
            "created_at": now,
            "updated_at": now,
            "created_by": "user123",
            "usage_count": 42,
            "avg_execution_time": 65,
            "variables": [
                {"name": "vpc_cidr", "type": "string", "default": "10.0.0.0/16", "required": True},
                {"name": "region", "type": "string", "default": "us-west-2", "required": True}
            ]
        }
    ]

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str):
    """
    Get details of a specific template
    """
    # Mock response - would fetch from DB
    now = datetime.now().isoformat()
    return {
        "id": template_id,
        "name": "AWS VPC",
        "description": "Basic AWS VPC setup",
        "tags": ["aws", "networking", "vpc"],
        "provider": "aws",
        "version": "1.0.0",
        "created_at": now,
        "updated_at": now,
        "created_by": "user123",
        "usage_count": 42,
        "avg_execution_time": 65,
        "variables": [
            {"name": "vpc_cidr", "type": "string", "default": "10.0.0.0/16", "required": True},
            {"name": "region", "type": "string", "default": "us-west-2", "required": True}
        ]
    }

@router.get("/{template_id}/files")
async def get_template_files(template_id: str):
    """
    Get list of files in a template
    """
    return {
        "template_id": template_id,
        "files": [
            "main.tf",
            "variables.tf",
            "outputs.tf"
        ]
    }

@router.get("/{template_id}/files/{file_path:path}")
async def get_template_file_content(template_id: str, file_path: str):
    """
    Get content of a specific file in a template
    """
    # Mock response with sample content
    if file_path == "main.tf":
        content = """
        resource "aws_vpc" "main" {
          cidr_block = var.vpc_cidr
          tags = {
            Name = "main-vpc"
          }
        }
        """
    else:
        content = "# Template file content would be here"
        
    return {
        "template_id": template_id,
        "file_path": file_path,
        "content": content
    } 