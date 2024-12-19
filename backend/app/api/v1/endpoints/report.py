from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.report import Report, ReportCreate
from app.services.report import ReportService
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Report)
def create_report(
    report_in: ReportCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Report:
    """Create a new report"""
    report_service = ReportService(db)
    return report_service.create_report(report_in, current_user.id)

@router.get("/{report_id}", response_model=Report)
def get_report(
    report_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Report:
    """Get a specific report"""
    report_service = ReportService(db)
    report = report_service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return report

@router.get("/", response_model=List[Report])
def list_reports(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> List[Report]:
    """List all reports for the current user"""
    report_service = ReportService(db)
    return report_service.list_user_reports(current_user.id)

@router.delete("/{report_id}")
def delete_report(
    report_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """Delete a report"""
    report_service = ReportService(db)
    report = report_service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    report_service.delete_report(report_id)
    return {"message": "Report deleted successfully"}
