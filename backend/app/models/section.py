from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

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
    
    # Content
    content = Column(Text)  # Final content
    uploaded_content = Column(Text)  # User uploaded/typed content
    ai_content = Column(Text)  # AI generated content
    
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
