from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TemplateVariable(BaseModel):
    name: str
    type: str
    default: Optional[Any] = None
    required: bool = False
    description: Optional[str] = None

class TemplateFileBase(BaseModel):
    filename: str
    content: str

class TemplateFileCreate(TemplateFileBase):
    pass

class TemplateFile(TemplateFileBase):
    id: str
    template_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    provider: str
    version: str
    tags: List[str] = []
    variables: List[Dict[str, Any]] = []

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    provider: Optional[str] = None
    version: Optional[str] = None
    tags: Optional[List[str]] = None
    variables: Optional[List[Dict[str, Any]]] = None

class Template(TemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime
    owner_id: str
    usage_count: int = 0
    avg_execution_time: Optional[int] = None

    class Config:
        orm_mode = True

class TemplateWithFiles(Template):
    files: List[TemplateFile] = []

    class Config:
        orm_mode = True 