from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base

class ReportStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Report(Base):
    __tablename__ = "reports"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(ReportStatus), nullable=False, default=ReportStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    user = relationship("User", back_populates="reports")
    chapters = relationship("Chapter", back_populates="report", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Report {self.title}>"
