from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
import json
from uuid import UUID

from app.api import deps
from app.models.section import Section
from app.models.user import User
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
    return {"message": "Content saved as context for AI generation"}

@router.post("/{section_id}/upload-content", 
    summary="Upload existing content to section",
    description="Upload existing content that will be used as context for AI generation"
)
async def upload_section_content(
    section_id: UUID,
    content: SectionContent,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Upload content as context for AI generation"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this section")
    
    section.uploaded_content = content.content
    db.commit()
    return {"message": "Content uploaded and saved as context"}

@router.post("/{section_id}/generate", 
    summary="Generate AI content for section",
    description="Generate final content using AI based on research and context"
)
async def generate_content(
    section_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Generate final content using AI"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this section")
    
    # Get context for AI generation
    context = {
        "report_title": section.chapter.report.title,
        "department": section.chapter.report.department,
        "chapter_number": section.chapter.chapter_number,
        "chapter_title": section.chapter.title,
        "section_number": section.section_number,
        "section_title": section.title,
        "user_context": {
            "typed_content": section.typed_content,
            "uploaded_content": section.uploaded_content
        }
    }
    
    final_content = generate_section_content(context)
    section.content = final_content
    db.commit()
    
    return {
        "message": "Content generated successfully",
        "content": section.content
    }

@router.get("/{section_id}/content", 
    response_model=SectionResponse,
    summary="Get section content",
    description="Get the final generated content for a section"
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
        raise HTTPException(status_code=403, detail="Not authorized to access this section")
    
    return {
        "id": section.id,
        "chapter_id": section.chapter_id,
        "section_number": section.section_number,
        "title": section.title,
        "content": section.content
    }

@router.post("/{section_id}/files", 
    response_model=FileUploadResponse,
    summary="Upload file to section",
    description="Upload images, diagrams, or other files for a section"
)
async def upload_file(
    section_id: UUID,
    file: UploadFile = File(...),
    position_data: str = Form(...),
    caption: str = Form(None),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Upload a file (image/diagram) to a section"""
    section = db.query(Section).filter(Section.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Verify user has access to this section's report
    if section.chapter.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this section")
    
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
    description="Get all files uploaded to a specific section"
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
        raise HTTPException(status_code=403, detail="Not authorized to access this section")
    
    files = db.query(FileUpload).filter(FileUpload.section_id == section_id).all()
    return [FileUploadResponse.from_orm(file) for file in files]
