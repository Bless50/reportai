from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class FileUpload(Base):
    """
    Model for tracking uploaded files (images) associated with sections.
    Handles positioning and metadata for proper report assembly.
    """
    __tablename__ = "file_uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    section_id = Column(UUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)
    
    # File information
    filename = Column(String, nullable=False)  # Original filename
    stored_filename = Column(String, nullable=False)  # How we store it (with UUID)
    file_type = Column(String, nullable=False)  # MIME type (image/jpeg, image/png, etc)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_path = Column(String, nullable=False)  # Where it's stored
    
    # Image specific data
    caption = Column(Text, nullable=True)  # Image caption/description
    position_data = Column(JSON, nullable=False)  # Stores positioning info like:
    # {
    #   "placement": "after_paragraph",
    #   "reference": "2",  # After 2nd paragraph
    #   "alignment": "center",
    #   "size": {"width": 500, "height": 300},
    #   "style": "figure"  # For academic styling
    # }
    
    # Upload metadata
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship
    section = relationship("Section", back_populates="files")

    def __repr__(self):
        return f"<FileUpload {self.filename} for section {self.section_id}>"
