from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.schemas.section import SectionResponse

class ChapterBase(BaseModel):
    """Base Chapter Schema"""
    chapter_number: int
    title: str

class ChapterCreate(ChapterBase):
    """Create Chapter Schema"""
    pass

class ChapterUpdate(ChapterBase):
    """Update Chapter Schema"""
    pass

class ChapterResponse(ChapterBase):
    """Response Chapter Schema"""
    id: UUID
    report_id: UUID
    sections: List[SectionResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
