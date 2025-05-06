from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class JobBase(BaseModel):
    job_type: str
    workspace: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = {}

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    execution_time: Optional[int] = None

class JobLog(BaseModel):
    log_entry: str
    level: str = "info"
    timestamp: datetime

    class Config:
        orm_mode = True

class Job(JobBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    owner_id: str
    template_id: Optional[str] = None
    execution_time: Optional[int] = None
    result: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class JobWithLogs(Job):
    logs: List[JobLog] = []

    class Config:
        orm_mode = True 