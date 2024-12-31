from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import logging

from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from app.services.auth import AuthService

router = APIRouter()
security_basic = HTTPBasic()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.post("/login", response_model=Token)
def login(
    credentials: HTTPBasicCredentials = Depends(security_basic),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get access token for user using email/password
    """
    try:
        logger.debug(f"Login attempt for user: {credentials.username}")
        auth_service = AuthService(db)
        user = auth_service.authenticate(
            email=credentials.username,
            password=credentials.password
        )
        
        if not user:
            logger.error(f"Invalid credentials for user: {credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
        
        logger.debug(f"Successfully generated token for user: {user.id}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
