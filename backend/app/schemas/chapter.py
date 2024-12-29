from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from .section import SectionResponse

class ChapterResponse(BaseModel):
    """Schema for reading chapter data with its sections"""
    id: UUID
    report_id: UUID
    chapter_number: int  # 1,2,3,4,5
    title: str
    sections: List[SectionResponse] = []

    class Config:
        from_attributes = True
