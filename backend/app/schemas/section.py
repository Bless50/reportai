from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.enums import ContentSourceType

class SectionBase(BaseModel):
    """Base Section Schema"""
    section_number: str = Field(..., description="Section number (e.g., '1.1', '1.2')")
    title: str = Field(..., description="Section title")
    level: int = Field(..., description="Section level (1 for main sections, 2 for subsections)")

class SectionCreate(SectionBase):
    """Schema for creating a new section"""
    chapter_id: UUID = Field(..., description="ID of the chapter this section belongs to")

class SectionUpdate(BaseModel):
    """Schema for updating an existing section"""
    section_number: Optional[str] = None
    title: Optional[str] = None
    level: Optional[int] = None

class SectionContent(BaseModel):
    """Schema for section content operations"""
    content: str = Field(..., description="Content text for the section")

class SectionInDB(SectionBase):
    """Schema for section in database"""
    id: UUID
    chapter_id: UUID
    user_content: Optional[str] = None
    ai_content: Optional[str] = None
    final_content: Optional[str] = None
    source_type: ContentSourceType = ContentSourceType.USER_UPLOADED
    word_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SectionResponse(SectionInDB):
    """Schema for reading section data"""
    has_files: bool = False
