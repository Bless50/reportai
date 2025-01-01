from .user import User
from .report import Report
from .chapter import Chapter
from .section import Section
from .file_upload import FileUpload
from .reference import Reference

# This ensures all models are imported and available for SQLAlchemy
__all__ = [
    "User",
    "Report",
    "Chapter",
    "Section",
    "FileUpload",
    "Reference"
]