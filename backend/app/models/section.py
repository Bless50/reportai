from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import ContentSourceType

class Section(Base):
    """
    Section model representing a section within a chapter.
    This is where the actual content lives.
    """
    __tablename__ = "sections"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    chapter_id = Column(PostgresUUID(as_uuid=True), ForeignKey("chapters.id"))
    
    # Section identifiers
    section_number = Column(String, nullable=False)  # e.g., "1.1", "1.1.1"
    title = Column(String, nullable=False)  # e.g., "Background of the study"
    level = Column(Integer, nullable=False)  # 1 for 1.1, 2 for 1.1.1
    
    # Content fields
    user_content = Column(Text)  # Content provided by user
    ai_content = Column(Text)  # AI generated content
    final_content = Column(Text)  # Final content after merging/editing
    source_type = Column(SQLEnum(ContentSourceType), nullable=False, default=ContentSourceType.USER_UPLOADED)
    
    # Metadata
    word_count = Column(Integer, default=0)
    format_requirements = Column(JSON)  # Store formatting requirements
    citations = Column(JSON)  # Store citations used
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="sections")
    files = relationship("FileUpload", back_populates="section", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Section {self.section_number}: {self.title}>"
