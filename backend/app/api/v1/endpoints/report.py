from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.models.user import User
from app.models.report import Report
from app.models.chapter import Chapter
from app.schemas.report import ReportCreate
from app.schemas.chapter import ChapterResponse
from app.services.report import ReportService

router = APIRouter()

@router.post("/", response_model=ReportCreate, status_code=status.HTTP_201_CREATED, summary="Create new report")
async def create_report(
    report_in: ReportCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Create a new report with predefined chapters"""
    report_service = ReportService(db)
    return report_service.create_report(current_user.id, report_in)

@router.get("/{report_id}", response_model=ReportCreate, summary="Get report with chapters")
async def get_report(
    report_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get a report with all its chapters and sections"""
    report_service = ReportService(db)
    return report_service.get_report(report_id, current_user.id)

@router.get("/{report_id}/chapters/{chapter_id}", response_model=ChapterResponse, summary="Get chapter with sections")
async def get_chapter(
    report_id: UUID,
    chapter_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get a specific chapter with all its sections"""
    # Verify report belongs to user
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Get chapter
    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id,
        Chapter.report_id == report_id
    ).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return chapter

@router.get("/", response_model=List[ReportCreate], summary="List all reports")
async def list_reports(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """List all reports for the current user"""
    report_service = ReportService(db)
    return report_service.list_reports(current_user.id)
