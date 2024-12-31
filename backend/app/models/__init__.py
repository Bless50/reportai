from app.models.user import User
from app.models.report import Report
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.file_upload import FileUpload

# This ensures all models are imported and available for SQLAlchemy
__all__ = [
    "User",
    "Report",
    "Chapter",
    "Section",
    "FileUpload"
]