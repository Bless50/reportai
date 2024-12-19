from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
)

# Create SessionLocal class with sessionmaker factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
