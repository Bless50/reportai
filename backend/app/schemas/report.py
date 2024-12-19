from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class ReportBase(BaseModel):
    """Base schema for Report with common attributes"""
    title: str
    department: str
    template_type: str = Field(default="default")
    custom_template: Optional[dict] = None

class ReportCreate(ReportBase):
    """Schema for creating a new report"""
    pass

class ReportInDB(ReportBase):
    """Schema for Report as stored in database"""
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True

class Report(ReportInDB):
    """Schema for Report response"""
    pass
