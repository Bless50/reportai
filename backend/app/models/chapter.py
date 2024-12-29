from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import ContentSourceType

class Chapter(Base):
    """
    Chapter model representing a chapter in a report.
    A chapter is essentially a container for sections.
    """
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)  # 1, 2, 3, etc.
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    report = relationship("Report", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chapter {self.chapter_number}: {self.title}>"
