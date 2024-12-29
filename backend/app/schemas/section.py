from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.enums import ContentSourceType

class SectionContent(BaseModel):
    """Schema for section content operations"""
    content: str = Field(..., description="Content text for the section")

class SectionUploadContent(BaseModel):
    """Schema for uploading existing content to a section"""
    content: str = Field(..., description="Content to upload to this section")

class SectionResponse(BaseModel):
    """Schema for reading section data"""
    id: UUID
    chapter_id: UUID
    section_number: str  # Already normalized (e.g., "1.1", "1.2")
    title: str
    content: Optional[str] = None
    uploaded_content: Optional[str] = None
    ai_content: Optional[str] = None
    source_type: ContentSourceType
    has_files: bool = False
    files_metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
