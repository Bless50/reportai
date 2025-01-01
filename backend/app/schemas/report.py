from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from app.models.report import ReportStatus
from app.schemas.chapter import ChapterResponse
from app.schemas.reference import ReferenceResponse

class ReportBase(BaseModel):
    """Base Report Schema"""
    title: str = Field(..., description="Report title")
    department: str = Field(..., description="Department or field of study")

    model_config = ConfigDict(from_attributes=True)

class ReportCreate(ReportBase):
    """Create Report Schema"""
    pass

class ReportUpdate(ReportBase):
    """Update Report Schema"""
    title: Optional[str] = Field(None, description="New report title")
    department: Optional[str] = Field(None, description="New department or field of study")

class ReportInDB(ReportBase):
    """Schema for Report as stored in database"""
    id: UUID
    user_id: UUID
    status: ReportStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReportResponse(ReportInDB):
    """Schema for Report response"""
    chapters: List[ChapterResponse] = []
    references: List[ReferenceResponse] = []
    status: str  # Changed to str to avoid validation issues

    model_config = ConfigDict(from_attributes=True)
