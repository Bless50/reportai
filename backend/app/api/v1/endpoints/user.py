# Import FastAPI components
from fastapi import APIRouter, Depends, HTTPException, status

# Import SQLAlchemy for database
from sqlalchemy.orm import Session
from datetime import datetime  # Add this import

# Import our dependencies
from ..deps import get_db, get_current_user, security_scheme # From deps.py we just created

# Import our schemas and models
from app.schemas import user as user_schemas  # Our Pydantic models
from app.core import security  # Our security utils
from app.models.user import User  # Our database model

# Create API router
router = APIRouter()

# Registration endpoint
@router.post("/register", response_model=user_schemas.UserResponse)
def create_user(
    *,  # Forces the use of named parameters
    db: Session = Depends(get_db),  # Get database session
    user_in: user_schemas.UserCreate  # Get user data from request body
):
    """
    Create new user (register).
    Example request body:
    {
        "email": "user@example.com",
        "password": "strongpass123",
        "full_name": "John Doe",
        "department": "Computer Science",
        "level": "HND",
        "institution": "My School"
    }
    """
    # Check if email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    # 1. Hash the password
    hashed_password = security.get_password_hash(user_in.password)
    
    # 2. Create user object
    user = User(
        email=user_in.email,
        password=hashed_password,  # Store hashed password
        full_name=user_in.full_name,
        level=user_in.level,
        institution=user_in.institution
    )
    
    # 3. Save to database
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

# Login endpoint
@router.post("/login", response_model=user_schemas.Token)
def login(
    *,
    db: Session = Depends(get_db),
    user_in: user_schemas.UserLogin
):
    """
    Login user and return access token.
    Example request body:
    {
        "email": "user@example.com",
        "password": "strongpass123"
    }
    """
    # Check if user exists and password is correct
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not security.verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
     # Update last_login time
    user.last_login = datetime.utcnow()
    db.commit()

    # Create access token
    access_token = security.create_access_token(data={"id": str(user.id)})
    
    # Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Get current user profile endpoint
@router.get("/me", response_model=user_schemas.UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user)  # Get current logged-in user
):
    """
    Get current user profile.
    Requires authentication token.
    """
    return current_user

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Logout current user."""
    # In a JWT-based auth system, we can't actually invalidate the token
    # But we can update the user's last_logout time for tracking
    return {"message": "Successfully logged out"}

@router.put("/me/update", response_model=user_schemas.UserResponse)
def update_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user_in: user_schemas.UserUpdate
):
    """Update current user's profile."""
    # Update user fields
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me/delete")
def delete_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete current user's account."""
    db.delete(current_user)
    db.commit()
    return {"message": "User successfully deleted"}