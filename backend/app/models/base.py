# import the necessary function from SQLALCHEMY
# declarative_base() is used to create a base class for our database models
from app.db.base_class import Base

# Import all models here that need to be discovered by Alembic
from app.models.user import User  # noqa
from app.models.report import Report  # noqa
from app.models.chapter import Chapter  # noqa
from app.models.section import Section  # noqa
from app.models.file_upload import FileUpload  # noqa