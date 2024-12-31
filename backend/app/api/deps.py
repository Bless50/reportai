from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import logging

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use HTTPBearer instead of OAuth2PasswordBearer
security = HTTPBearer()

def get_db() -> Generator:
    """
    Get database session.
    """
    db = None
    try:
        db = SessionLocal()
        logger.debug("Created new database session")
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        if db:
            logger.debug("Closing database session")
            db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    token: HTTPBearer = Depends(security)
) -> User:
    """
    Get current user from JWT token
    """
    try:
        logger.debug("Authenticating user from token")
        
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Use token.credentials to get the actual token string
            payload = jwt.decode(
                token.credentials,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                logger.error("Token missing sub claim")
                raise credentials_exception
        except JWTError as e:
            logger.error(f"JWT decode error: {str(e)}")
            raise credentials_exception

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            logger.error(f"User not found: {user_id}")
            raise credentials_exception

        logger.debug(f"Successfully authenticated user: {user.id}")
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise
