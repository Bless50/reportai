from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ReportAI"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Debug mode
    DEBUG: bool = True
    
    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/reportai_db"

    class Config:
        case_sensitive = True
        env_file = ".env"

# Create settings instance
settings = Settings()
