from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
import json
from uuid import UUID

from app.api import deps
from app.models.section import Section
from app.models.user import User
from app.schemas.section import SectionContent, SectionResponse, SectionInDB
from app.schemas.file_upload import FileUploadResponse
from app.core.content_generation import generate_section_content

router = APIRouter(
    prefix="/sections",
    tags=["content-management"]
)

@router.post("/{section_id}/type-content", 
    response_model=SectionResponse,
    summary="Add typed content to section",
    description="Add manually typed content that will be used as context for AI generation"
)
async def add_typed_content(
    section_id: UUID,
    content: SectionContent,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Add typed content as context for AI generation"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this section")
    
    section.typed_content = content.content
    db.commit()
    db.refresh(section)
    return section

@router.post("/{section_id}/upload-content", 
    response_model=SectionResponse,
    summary="Upload existing content to section",
    description="Upload existing content that will be used as context for AI generation"
)
async def upload_section_content(
    section_id: UUID,
    content: SectionContent,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Upload existing content as context for AI generation"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this section")
    
    section.uploaded_content = content.content
    db.commit()
    db.refresh(section)
    return section

@router.get("/{section_id}/content",
    response_model=SectionResponse,
    summary="Get section content",
    description="Get the final content for a section"
)
async def get_section_content(
    section_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Get the final content for a section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this section")
    
    return section

@router.post("/{section_id}/generate",
    response_model=SectionResponse,
    summary="Generate content for section",
    description="Generate content for section using AI"
)
async def generate_content(
    section_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Generate content for a section using AI"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this section")
    
    # Generate content using AI
    generated_content = await generate_section_content(section)
    section.ai_content = generated_content
    section.content = generated_content  # Set as final content
    
    db.commit()
    db.refresh(section)
    return section

@router.post("/{section_id}/files",
    response_model=FileUploadResponse,
    summary="Upload file to section",
    description="Upload a file (image/diagram) to a section"
)
async def upload_file(
    section_id: UUID,
    file: UploadFile = File(...),
    position_data: str = Form(...),
    caption: str = Form(None),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Upload a file to a section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this section")
    
    # Process file upload
    try:
        position = json.loads(position_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid position data format")
    
    # TODO: Implement file upload logic
    # For now, just return a mock response
    return {
        "id": UUID('00000000-0000-0000-0000-000000000000'),
        "filename": file.filename,
        "file_type": file.content_type,
        "position": position,
        "caption": caption
    }

@router.get("/{section_id}/files",
    response_model=List[FileUploadResponse],
    summary="Get section files",
    description="Get all files uploaded to a section"
)
async def get_section_files(
    section_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Get all files uploaded to a section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this section")
    
    # TODO: Implement file retrieval logic
    # For now, just return an empty list
    return []