from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class ReferenceBase(BaseModel):
    """Base Reference Schema"""
    citation_key: str = Field(..., description="Unique identifier for the reference")
    reference_type: str = Field(..., description="Type of reference (article, book, website)")
    authors: List[str] = Field(..., description="List of authors in format 'Last, F.'")
    year: int = Field(..., description="Publication year")
    title: str = Field(..., description="Title of the work")
    
    # Optional fields based on reference type
    journal: Optional[str] = Field(None, description="Journal name for articles")
    volume: Optional[str] = Field(None, description="Volume number")
    issue: Optional[str] = Field(None, description="Issue number")
    pages: Optional[str] = Field(None, description="Page range")
    
    edition: Optional[str] = Field(None, description="Edition number for books")
    publisher: Optional[str] = Field(None, description="Publisher name")
    publisher_location: Optional[str] = Field(None, description="Publisher location")
    
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    url: Optional[str] = Field(None, description="URL for online sources")

    model_config = ConfigDict(from_attributes=True)

class ReferenceCreate(ReferenceBase):
    """Create Reference Schema"""
    report_id: UUID = Field(..., description="ID of the report this reference belongs to")

class ReferenceUpdate(ReferenceBase):
    """Update Reference Schema"""
    citation_key: Optional[str] = None
    reference_type: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    title: Optional[str] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    edition: Optional[str] = None
    publisher: Optional[str] = None
    publisher_location: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ReferenceInDB(ReferenceBase):
    """Database Reference Schema"""
    id: UUID
    report_id: UUID
    created_at: datetime
    updated_at: datetime
    in_text_citation: str = Field(..., description="In-text citation format (e.g., 'Smith et al., 2020')")

    model_config = ConfigDict(from_attributes=True)

class ReferenceResponse(ReferenceInDB):
    """Response Reference Schema"""
    formatted_apa: str = Field(..., description="Reference formatted in APA style")

    model_config = ConfigDict(from_attributes=True)

class ReferencePageResponse(BaseModel):
    """Response model for the generated references page"""
    report_id: UUID
    references_content: str
    model_config = ConfigDict(from_attributes=True)
