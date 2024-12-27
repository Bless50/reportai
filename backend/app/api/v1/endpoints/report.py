from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.report import Report, ReportCreate, ReportUpdate
from app.services.report import ReportService

router = APIRouter()

@router.get("/{report_id}", response_model=Report)
def get_report(
    report_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Report:
    """Get a specific report by ID"""
    report_service = ReportService(db)
    report = report_service.get_report(report_id, current_user.id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report

@router.get("/", response_model=List[Report])
def list_reports(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> List[Report]:
    """List all reports for current user"""
    report_service = ReportService(db)
    return report_service.list_user_reports(current_user.id)

@router.post("/", response_model=Report, status_code=status.HTTP_201_CREATED)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Report:
    """Create a new report"""
    report_service = ReportService(db)
    return report_service.create_report(report_in, current_user.id)

@router.put("/{report_id}", response_model=Report)
def update_report(
    report_id: UUID,
    report_in: ReportUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Report:
    """Update an existing report"""
    report_service = ReportService(db)
    report = report_service.get_report(report_id, current_user.id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report_service.update_report(report_id, current_user.id, report_in)

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(
    report_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> None:
    """Delete a report"""
    report_service = ReportService(db)
    report = report_service.get_report(report_id, current_user.id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    report_service.delete_report(report_id, current_user.id)
