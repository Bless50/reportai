from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
import json

from app.api import deps
from app.models.section import Section
from app.models.file_upload import FileUpload
from app.schemas.section import SectionContent, SectionResponse
from app.schemas.file_upload import FileUploadResponse
from app.core.content_generation import generate_section_content

router = APIRouter(
    prefix="/sections",
    tags=["content-management"],
    responses={404: {"description": "Section not found"}}
)

@router.post("/{section_id}/type-content", 
    summary="Add typed content to section",
    description="Add or update manually typed content for a specific section")
async def add_typed_content(
    section_id: str,
    content: SectionContent,
    db: Session = Depends(deps.get_db),
):
    """Add or update typed content for a section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    section.uploaded_content = content.content
    section.content = content.content  # Update main content
    db.commit()
    return {"message": "Content updated successfully"}

@router.post("/{section_id}/upload-content", 
    summary="Upload existing content to section",
    description="Upload pre-existing content for a specific section")
async def upload_section_content(
    section_id: str,
    content: SectionContent,
    db: Session = Depends(deps.get_db),
):
    """Upload existing content for a section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    section.uploaded_content = content.content
    section.content = content.content  # Update main content
    db.commit()
    return {"message": "Content uploaded successfully"}

@router.post("/{section_id}/generate", 
    summary="Generate AI content for section",
    description="Use AI to generate content for a specific section")
async def generate_content(
    section_id: str,
    db: Session = Depends(deps.get_db),
):
    """Generate AI content for a section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Generate content using AI
    generated_content = generate_section_content(section)
    section.ai_content = generated_content
    section.content = generated_content  # Update main content
    db.commit()
    return {"message": "Content generated successfully", "content": generated_content}

@router.get("/{section_id}/content", 
    response_model=SectionResponse,
    summary="Get section content",
    description="Get all content (typed, uploaded, AI-generated) for a specific section")
async def get_section_content(
    section_id: str,
    db: Session = Depends(deps.get_db),
):
    """Get section content including uploaded and AI-generated content"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    return SectionResponse.from_orm(section)

@router.post("/{section_id}/files", 
    response_model=FileUploadResponse,
    summary="Upload file to section",
    description="Upload a file (image) with position data to a specific section")
async def upload_file(
    section_id: str,
    file: UploadFile = File(...),
    position_data: str = Form(...),  # JSON string with position info
    caption: str = Form(None),
    db: Session = Depends(deps.get_db),
):
    """Upload a file (image) to a section with position data"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Parse position data
    try:
        position = json.loads(position_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid position data format")
    
    # Create file upload record
    file_upload = FileUpload(
        section_id=section_id,
        filename=file.filename,
        file_type=file.content_type,
        file_size=0,  # Will be updated after saving
        position_data=position,
        caption=caption
    )
    
    # Save file and update size
    # TODO: Implement actual file storage
    
    db.add(file_upload)
    db.commit()
    db.refresh(file_upload)
    
    return FileUploadResponse.from_orm(file_upload)

@router.get("/{section_id}/files", 
    response_model=List[FileUploadResponse],
    summary="Get section files",
    description="Get all files uploaded to a specific section")
async def get_section_files(
    section_id: str,
    db: Session = Depends(deps.get_db),
):
    """Get all files uploaded to a section"""
    files = db.query(FileUpload).filter(FileUpload.section_id == section_id).all()
    return [FileUploadResponse.from_orm(file) for file in files]
