from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging

from app.core.database import SessionLocal
from app.core import security
from app.models.user import User

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

security_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> User:
    """Get current user from token"""
    # Get token from authorization header
    token = credentials.credentials
    logger.debug(f"Received token: {token[:10]}...")  # Log first 10 chars of token
    
    # Decode token
    payload = security.decode_token(token)
    logger.debug(f"Decoded payload: {payload}")  # Log decoded payload
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.query(User).filter(User.id == payload.get("id")).first()
    logger.debug(f"Found user: {user}")  # Log user object
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
    