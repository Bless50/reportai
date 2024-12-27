from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging
from uuid import UUID

from app.core.database import SessionLocal
from app.core import security
from app.models.user import User

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# OAuth2 scheme for token handling
security_scheme = HTTPBearer(
    auto_error=True,
    scheme_name="Authorization"
)

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> User:
    """
    Get current user from token.
    This dependency will be used to protect routes that require authentication.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Get token from authorization header
        token = credentials.credentials
        logger.debug(f"Validating token: {token[:10]}...")
        
        # Decode token
        payload = security.decode_token(token)
        user_id = payload.get("sub")
        
        if user_id is None:
            logger.error("Token payload missing 'sub' claim")
            raise credentials_exception
            
        # Convert string UUID to UUID object
        try:
            user_id = UUID(user_id)
        except ValueError:
            logger.error(f"Invalid UUID format in token: {user_id}")
            raise credentials_exception
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            logger.error(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
            
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise credentials_exception