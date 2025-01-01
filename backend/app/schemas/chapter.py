from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.schemas.section import SectionResponse

class ChapterBase(BaseModel):
    """Base Chapter Schema"""
    chapter_number: int
    title: str

    model_config = ConfigDict(from_attributes=True)

class ChapterCreate(ChapterBase):
    """Create Chapter Schema"""
    report_id: UUID

class ChapterUpdate(ChapterBase):
    """Update Chapter Schema"""
    chapter_number: Optional[int] = None
    title: Optional[str] = None

class ChapterInDB(ChapterBase):
    """Database Chapter Schema"""
    id: UUID
    report_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ChapterResponse(ChapterInDB):
    """Response Chapter Schema"""
    sections: List[SectionResponse] = []

    model_config = ConfigDict(from_attributes=True)
