from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    templates = relationship("Template", back_populates="owner")
    jobs = relationship("Job", back_populates="owner")

class Template(Base):
    __tablename__ = "templates"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    provider = Column(String, index=True)
    version = Column(String)
    tags = Column(JSON, default=list)
    variables = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(String, ForeignKey("users.id"))
    usage_count = Column(Integer, default=0)
    avg_execution_time = Column(Integer, nullable=True)

    owner = relationship("User", back_populates="templates")
    files = relationship("TemplateFile", back_populates="template")
    jobs = relationship("Job", back_populates="template")

class TemplateFile(Base):
    __tablename__ = "template_files"

    id = Column(String, primary_key=True, default=generate_uuid)
    template_id = Column(String, ForeignKey("templates.id"))
    filename = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    template = relationship("Template", back_populates="files")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=generate_uuid)
    job_type = Column(String, index=True)
    workspace = Column(String, index=True)
    description = Column(Text, nullable=True)
    parameters = Column(JSON)
    status = Column(String, index=True)  # pending, running, completed, failed, cancelled
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(String, ForeignKey("users.id"))
    template_id = Column(String, ForeignKey("templates.id"), nullable=True)
    execution_time = Column(Integer, nullable=True)  # in seconds

    owner = relationship("User", back_populates="jobs")
    template = relationship("Template", back_populates="jobs")
    logs = relationship("JobLog", back_populates="job")

class JobLog(Base):
    __tablename__ = "job_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    job_id = Column(String, ForeignKey("jobs.id"))
    log_entry = Column(Text)
    level = Column(String)  # info, warning, error
    timestamp = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="logs") 