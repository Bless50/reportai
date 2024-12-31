# Import all SQLAlchemy models here
from app.db.base_class import Base
from app.models.user import User
from app.models.report import Report
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.file_upload import FileUpload

# This allows Alembic to detect all models when generating migrations
