from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import logging

from app.api import deps
from app.models.user import User
from app.models.report import Report
from app.models.chapter import Chapter
from app.schemas.report import ReportCreate, ReportResponse
from app.schemas.chapter import ChapterResponse
from app.services.report import ReportService

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["report-management"],
    responses={404: {"description": "Report not found"}}
)

@router.post("/", 
    response_model=ReportResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Create new report",
    description="Create a new report with predefined chapters",
    tags=["report-management"]
)
async def create_report(
    report_in: ReportCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Create a new report with predefined chapters"""
    try:
        logger.info(f"Creating report for user {current_user.id}")
        logger.debug(f"Report data: {report_in.dict()}")
        
        report_service = ReportService(db)
        report = report_service.create_report(report_in, current_user.id)
        
        logger.info(f"Successfully created report {report.id}")
        return report
        
    except Exception as e:
        logger.error(f"Error creating report: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating report: {str(e)}"
        )

@router.get("/", 
    response_model=List[ReportResponse], 
    summary="List all reports",
    description="Get all reports for the current user",
    tags=["report-management"]
)
async def list_reports(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """List all reports for the current user"""
    try:
        logger.info(f"Listing reports for user {current_user.id}")
        report_service = ReportService(db)
        reports = report_service.list_user_reports(current_user.id)
        logger.info(f"Found {len(reports)} reports")
        return reports
    except Exception as e:
        logger.error(f"Error listing reports: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing reports: {str(e)}"
        )

@router.get("/{report_id}", 
    response_model=ReportResponse, 
    summary="Get report with chapters",
    description="Get a specific report with all its chapters",
    tags=["report-management"]
)
async def get_report(
    report_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get a specific report with all its chapters"""
    try:
        logger.info(f"Getting report {report_id} for user {current_user.id}")
        report_service = ReportService(db)
        report = report_service.get_report(report_id, current_user.id)
        logger.info(f"Successfully retrieved report {report_id}")
        return report
    except Exception as e:
        logger.error(f"Error getting report: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting report: {str(e)}"
        )

@router.get("/{report_id}/chapters/{chapter_id}", 
    response_model=ChapterResponse,
    summary="Get chapter with sections",
    description="Get a specific chapter with all its sections",
    tags=["report-management"]
)
async def get_chapter(
    report_id: UUID,
    chapter_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Get a specific chapter with all its sections"""
    try:
        logger.info(f"Getting chapter {chapter_id} for report {report_id} and user {current_user.id}")
        report_service = ReportService(db)
        report = report_service.get_report(report_id, current_user.id)
        
        # Find the specific chapter
        chapter = db.query(Chapter).filter(
            Chapter.id == chapter_id,
            Chapter.report_id == report_id
        ).first()
        
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        logger.info(f"Successfully retrieved chapter {chapter_id}")
        return chapter
    except Exception as e:
        logger.error(f"Error getting chapter: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting chapter: {str(e)}"
        )

@router.delete("/{report_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete report",
    description="Delete a report and all its chapters and sections",
    tags=["report-management"]
)
async def delete_report(
    report_id: UUID,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """Delete a report and all its associated data"""
    try:
        logger.info(f"Deleting report {report_id} for user {current_user.id}")
        report_service = ReportService(db)
        report_service.delete_report(report_id, current_user.id)
        logger.info(f"Successfully deleted report {report_id}")
    except Exception as e:
        logger.error(f"Error deleting report: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting report: {str(e)}"
        )
