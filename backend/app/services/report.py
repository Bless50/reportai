from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.models.report import Report, ReportStatus
from app.models.chapter import Chapter
from app.models.section import Section
from app.schemas.report import ReportCreate, ReportUpdate

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_report(self, report_id: UUID, user_id: UUID) -> Optional[Report]:
        """Get a specific report by ID"""
        logger.debug(f"Getting report with ID: {report_id}, user ID: {user_id}")
        report = self.db.query(Report).filter(
            Report.id == report_id,
            Report.user_id == user_id
        ).first()
        
        if not report:
            logger.error(f"Report not found with ID: {report_id}, user ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        logger.debug(f"Found report with ID: {report_id}, user ID: {user_id}")
        return report

    def list_user_reports(self, user_id: UUID) -> List[Report]:
        """List all reports for a user"""
        logger.debug(f"Listing reports for user ID: {user_id}")
        reports = self.db.query(Report).filter(Report.user_id == user_id).all()
        logger.debug(f"Found {len(reports)} reports for user ID: {user_id}")
        return reports

    def create_report(self, report_in: ReportCreate, user_id: UUID) -> Report:
        """Create a new report with predefined chapters and sections"""
        try:
            logger.debug(f"Creating report with title: {report_in.title}, department: {report_in.department}")
            
            # Create report
            db_report = Report(
                title=report_in.title,
                department=report_in.department,
                user_id=user_id,
                status=ReportStatus.DRAFT.value  # Use .value to get string
            )
            self.db.add(db_report)
            
            try:
                self.db.flush()  # Get report ID without committing
                logger.debug(f"Created report with ID: {db_report.id}")
            except Exception as flush_error:
                logger.error(f"Error during flush: {str(flush_error)}")
                raise

            # Create predefined chapters
            chapters = [
                {"number": 1, "title": "INTRODUCTION"},
                {"number": 2, "title": "LITERATURE REVIEW"},
                {"number": 3, "title": "METHODOLOGY AND PRESENTATION OF INTERNSHIP ACTIVITIES"},
                {"number": 4, "title": "PRESENTATION, ANALYSIS AND INTERPRETATION OF DATA"},
                {"number": 5, "title": "SUMMARY OF FINDINGS, CONCLUSION AND RECOMMENDATIONS"}
            ]

            for chapter_data in chapters:
                try:
                    chapter = Chapter(
                        report_id=db_report.id,
                        chapter_number=chapter_data["number"],
                        title=chapter_data["title"]
                    )
                    self.db.add(chapter)
                    self.db.flush()
                    logger.debug(f"Created chapter {chapter_data['number']}: {chapter_data['title']}")

                    # Create sections based on chapter number
                    sections = self._get_chapter_sections(chapter_data["number"])
                    for section_data in sections:
                        section = Section(
                            chapter_id=chapter.id,
                            section_number=section_data["number"],
                            title=section_data["title"],
                            level=section_data.get("level", 1)
                        )
                        self.db.add(section)
                        
                except Exception as chapter_error:
                    logger.error(f"Error creating chapter {chapter_data['number']}: {str(chapter_error)}")
                    raise

            try:
                self.db.commit()
                self.db.refresh(db_report)
                logger.debug("Successfully committed report and all related entities")
                return db_report
            except Exception as commit_error:
                logger.error(f"Error during commit: {str(commit_error)}")
                raise
            
        except Exception as e:
            logger.error(f"Error creating report: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating report: {str(e)}"
            )

    def _get_chapter_sections(self, chapter_number: int) -> List[dict]:
        """Get predefined sections for each chapter"""
        logger.debug(f"Getting sections for chapter number: {chapter_number}")
        sections_map = {
            1: [  # Chapter 1 sections
                {"number": "1.1", "title": "Background of the study", "level": 1},
                {"number": "1.1.1", "title": "Historical background", "level": 2},
                {"number": "1.1.2", "title": "Theoretical background", "level": 2},
                {"number": "1.1.3", "title": "Conceptual background", "level": 2},
                {"number": "1.1.4", "title": "Contextual background", "level": 2},
                {"number": "1.2", "title": "Problem Statement", "level": 1},
                {"number": "1.3", "title": "Research Objectives", "level": 1},
                {"number": "1.3.1", "title": "Main Research Objective", "level": 2},
                {"number": "1.3.2", "title": "Specific Research Objectives", "level": 2},
                {"number": "1.4", "title": "Research Questions", "level": 1},
                {"number": "1.4.1", "title": "Main Research Questions", "level": 2},
                {"number": "1.4.2", "title": "Specific Research Questions", "level": 2},
                {"number": "1.5", "title": "Justification of the study", "level": 1},
                {"number": "1.6", "title": "Signification of the study", "level": 1},
                {"number": "1.7", "title": "Scope of the study", "level": 1},
                {"number": "1.8", "title": "Limitation of the study", "level": 1},
                {"number": "1.9", "title": "Definition of terms", "level": 1}
            ],
            2: [  # Chapter 2 sections
                {"number": "2.1", "title": "Reviews by Theory", "level": 1},
                {"number": "2.2", "title": "Reviews by concept", "level": 1},
                {"number": "2.3", "title": "Other Reviews", "level": 1}
            ],
            3: [  # Chapter 3 sections
                {"number": "3.1", "title": "Research design", "level": 1},
                {"number": "3.2", "title": "Population, sample size and techniques", "level": 1},
                {"number": "3.3", "title": "Sources of data collection", "level": 1},
                {"number": "3.4", "title": "Method of data analysis", "level": 1},
                {"number": "3.5", "title": "Internship activities", "level": 1},
                {"number": "3.6", "title": "Difficulties in carrying out assigned tasks", "level": 1},
                {"number": "3.7", "title": "Skills Acquired", "level": 1}
            ],
            4: [  # Chapter 4 sections
                {"number": "4.1", "title": "Data Presentation", "level": 1},
                {"number": "4.2", "title": "Data Analysis", "level": 1},
                {"number": "4.3", "title": "Interpretation of Results", "level": 1}
            ],
            5: [  # Chapter 5 sections
                {"number": "5.1", "title": "Summary of Findings", "level": 1},
                {"number": "5.2", "title": "Conclusion", "level": 1},
                {"number": "5.3", "title": "Recommendations", "level": 1}
            ]
        }
        logger.debug(f"Found {len(sections_map.get(chapter_number, []))} sections for chapter number: {chapter_number}")
        return sections_map.get(chapter_number, [])

    def update_report(self, report_id: UUID, user_id: UUID, report_in: ReportUpdate) -> Report:
        """Update an existing report"""
        logger.debug(f"Updating report with ID: {report_id}, user ID: {user_id}")
        report = self.get_report(report_id, user_id)
        
        update_data = report_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(report, field, value)
            
        try:
            self.db.commit()
            self.db.refresh(report)
            logger.debug(f"Successfully updated report with ID: {report_id}, user ID: {user_id}")
            return report
        except Exception as e:
            logger.error(f"Error updating report: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating report: {str(e)}"
            )

    def delete_report(self, report_id: UUID, user_id: UUID) -> None:
        """Delete a report and all its associated data"""
        logger.debug(f"Deleting report with ID: {report_id}, user ID: {user_id}")
        report = self.get_report(report_id, user_id)
        if not report:
            logger.error(f"Report not found with ID: {report_id}, user ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        try:
            self.db.delete(report)  # This will cascade delete chapters and sections
            self.db.commit()
            logger.debug(f"Successfully deleted report with ID: {report_id}, user ID: {user_id}")
            return {"message": "Report deleted successfully"}
        except Exception as e:
            logger.error(f"Error deleting report: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting report: {str(e)}"
            )
