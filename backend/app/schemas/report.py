from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

# Import ReportStatus from models
from app.models.report import ReportStatus
from app.schemas.chapter import ChapterResponse

class ReportBase(BaseModel):
    """Base Report Schema"""
    title: str = Field(..., description="Report title")
    department: str = Field(..., description="Department or field of study")

class ReportCreate(ReportBase):
    """Create Report Schema"""
    pass

class ReportUpdate(ReportBase):
    """Update Report Schema"""
    pass

class ReportResponse(ReportBase):
    """Response Report Schema"""
    id: UUID
    user_id: UUID
    chapters: List[ChapterResponse] = []
    created_at: datetime
    updated_at: datetime
    status: str  # Changed to str to avoid validation issues

    class Config:
        from_attributes = True

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
