from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy.orm import relationship
import enum

from .base import Base

class ReportStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TemplateType(str, enum.Enum):
    DEFAULT = "default"
    CUSTOM = "custom"

class Report(Base):
    __tablename__ = "reports"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    template_type = Column(SQLAlchemyEnum(TemplateType), nullable=False, default=TemplateType.DEFAULT)
    custom_template = Column(JSONB, nullable=True)  # Only used when template_type is CUSTOM
    status = Column(SQLAlchemyEnum(ReportStatus), nullable=False, default=ReportStatus.DRAFT)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="reports")
    chapters = relationship("Chapter", back_populates="report", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Report {self.title}>"
