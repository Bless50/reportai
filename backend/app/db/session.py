from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # Create database engine
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,  # Enable connection pool "pre-ping" feature
        echo=True  # Enable SQL logging
    )
    
    # Test the connection
    with engine.connect() as connection:
        logger.info("Successfully connected to the database")
        
except SQLAlchemyError as e:
    logger.error(f"Database connection error: {str(e)}")
    raise

# Create SessionLocal class with sessionmaker factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Prevent detached instance errors
)
