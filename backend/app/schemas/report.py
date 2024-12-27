from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from enum import Enum

class ReportStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ReportBase(BaseModel):
    """Base schema for Report with common attributes"""
    title: str
    department: str

class ReportCreate(ReportBase):
    """Schema for creating a new report"""
    pass

class ReportUpdate(ReportBase):
    """Schema for updating an existing report"""
    title: Optional[str] = None
    department: Optional[str] = None
    status: Optional[ReportStatus] = None

class ReportInDB(ReportBase):
    """Schema for Report as stored in database"""
    id: UUID
    status: ReportStatus
    created_at: datetime
    updated_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True

class Report(ReportInDB):
    """Schema for Report response"""
    pass
