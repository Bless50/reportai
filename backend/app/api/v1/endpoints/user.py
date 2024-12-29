from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas import user as schemas
from datetime import datetime
from jose import jwt
from app.core.config import settings

router = APIRouter()

@router.post(
    "/register", 
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with the required information",
    tags=["authentication"]
)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Create new user with the following fields:
    - **email**: required, valid email format
    - **password**: required, min length 8
    - **full_name**: required, min length 2
    - **level**: required (e.g., HND, BSc)
    - **institution**: required
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        password=hashed_password,
        full_name=user_in.full_name,
        level=user_in.level,
        institution=user_in.institution
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post(
    "/login", 
    response_model=schemas.Token,
    summary="Login user",
    description="Login with email and password to get access token",
    tags=["authentication"]
)
async def login(
    user_in: schemas.UserLogin,
    db: Session = Depends(deps.get_db)
):
    """
    Login with the following fields:
    - **email**: required, valid email format
    - **password**: required, min length 8

    Returns:
    - **access_token**: JWT token for Bearer authentication
    - **token_type**: bearer
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()

    # Create minimal token with just the user ID
    access_token = jwt.encode(
        {"sub": str(user.id)},  # Using "sub" as it's standard for JWT
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get(
    "/me", 
    response_model=schemas.UserResponse,
    summary="Get current user",
    description="Get current user profile information",
    tags=["profile"]
)
async def read_user_me(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get current authenticated user's profile.
    Requires Bearer token authentication.
    """
    return current_user

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Logout current user",
    tags=["authentication"]
)
async def logout(current_user: User = Depends(deps.get_current_user)):
    """
    Logout current authenticated user.
    Requires Bearer token authentication.
    """
    return {"message": "Successfully logged out"}

@router.put(
    "/me", 
    response_model=schemas.UserResponse,
    summary="Update current user",
    description="Update current user's profile information",
    tags=["profile"]
)
async def update_user(
    user_in: schemas.UserUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Update current user profile with optional fields.
    Requires Bearer token authentication.
    
    Fields:
    - **full_name**: optional, min length 2
    - **level**: optional (e.g., HND, BSc)
    - **institution**: optional
    - **password**: optional, min length 8
    """
    for field, value in user_in.dict(exclude_unset=True).items():
        if field == "password":
            value = get_password_hash(value)
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete current user",
    description="Delete current user's account",
    tags=["profile"]
)
async def delete_user(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Delete current authenticated user's account.
    Requires Bearer token authentication.
    """
    db.delete(current_user)
    db.commit()
    return None