from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
import uuid

# Get database URL from environment variable
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/reportai_db"

# Create SQLAlchemy engine with UUID type handling
engine = create_engine(
    DATABASE_URL,
    json_serializer=lambda obj: obj.hex if isinstance(obj, uuid.UUID) else str(obj)
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()