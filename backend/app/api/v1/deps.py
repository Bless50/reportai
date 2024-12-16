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
    try:
        # Get token from authorization header
        token = credentials.credentials
        # Remove 'Bearer' if it's in the token
        if token.startswith('Bearer '):
            token = token.replace('Bearer ', '')
            
        logger.debug(f"Processing token: {token[:10]}...")
        
        # Decode token
        payload = security.decode_token(token)
        logger.debug(f"Decoded payload: {payload}")
        
        user_id = payload.get("sub")  # Get user_id from "sub" claim
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )