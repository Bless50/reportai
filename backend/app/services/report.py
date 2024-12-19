from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from app.models.report import Report
from app.schemas.report import ReportCreate

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def create_report(self, report_data: ReportCreate, user_id: UUID) -> Report:
        """Create a new report"""
        db_report = Report(
            **report_data.model_dump(),
            user_id=user_id
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        return db_report

    def get_report(self, report_id: UUID) -> Optional[Report]:
        """Get a specific report by ID"""
        return self.db.query(Report).filter(Report.id == report_id).first()

    def list_user_reports(self, user_id: UUID) -> List[Report]:
        """List all reports for a specific user"""
        return self.db.query(Report).filter(Report.user_id == user_id).all()

    def delete_report(self, report_id: UUID) -> bool:
        """Delete a report by ID"""
        report = self.get_report(report_id)
        if report:
            self.db.delete(report)
            self.db.commit()
            return True
        return False
