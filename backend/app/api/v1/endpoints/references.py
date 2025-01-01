from typing import List
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.api import deps
from app.models import User, Reference, Report
from app.core.content_generation import generate_references_page
from app.schemas.reference import ReferenceResponse, ReferencePageResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["references"],
    responses={404: {"description": "Reference not found"}}
)

@router.get("/{reference_id}", 
    response_model=ReferenceResponse,
    summary="Get reference",
    description="Get a specific reference by ID"
)
async def get_reference(
    reference_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get a specific reference"""
    reference = db.query(Reference).filter(Reference.id == reference_id).first()
    if not reference:
        raise HTTPException(status_code=404, detail="Reference not found")
    
    # Verify user has access to this reference's report
    if reference.report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this reference")
    
    return reference

@router.get("/report/{report_id}", 
    response_model=List[ReferenceResponse],
    summary="Get report references",
    description="Get all references for a specific report"
)
async def get_report_references(
    report_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get all references for a report"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report.references

@router.post("/generate/{report_id}",
    response_model=ReferencePageResponse,
    summary="Generate references page",
    description="Generate the references page for a report based on citations"
)
async def generate_references_page_endpoint(
    report_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Generate references page for a report"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Generate references page using AI
    references_content = await generate_references_page(report)
    
    # Update report's references
    report.references_content = references_content
    db.commit()
    db.refresh(report)
    
    return {
        "report_id": report.id,
        "references_content": references_content
    }
