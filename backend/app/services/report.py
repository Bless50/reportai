from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_report(self, report_id: UUID, user_id: UUID) -> Optional[Report]:
        """Get a specific report by ID"""
        report = self.db.query(Report).filter(
            Report.id == report_id,
            Report.user_id == user_id
        ).first()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        return report

    def list_user_reports(self, user_id: UUID) -> List[Report]:
        """List all reports for a user"""
        return self.db.query(Report).filter(Report.user_id == user_id).all()

    def create_report(self, report_in: ReportCreate, user_id: UUID) -> Report:
        """Create a new report"""
        db_report = Report(
            title=report_in.title,
            department=report_in.department,
            user_id=user_id
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def update_report(self, report_id: UUID, user_id: UUID, report_in: ReportUpdate) -> Report:
        """Update an existing report"""
        report = self.get_report(report_id, user_id)
        
        update_data = report_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(report, field, value)
            
        self.db.commit()
        self.db.refresh(report)
        return report

    def delete_report(self, report_id: UUID, user_id: UUID) -> None:
        """Delete a report"""
        report = self.get_report(report_id, user_id)
        self.db.delete(report)
        self.db.commit()
