from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class FileUploadBase(BaseModel):
    """Base schema for file upload data"""
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="MIME type of the file")
    file_size: int = Field(..., description="Size of file in bytes")

class FileUploadCreate(FileUploadBase):
    """Schema for creating a new file upload record"""
    section_id: UUID = Field(..., description="ID of the section this file belongs to")

class FileUploadResponse(FileUploadBase):
    """Schema for file upload response"""
    id: UUID
    section_id: UUID
    uploaded_at: datetime

    class Config:
        from_attributes = True
