from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    """Base user schema with common attributes"""
    email: EmailStr = Field(
        ..., 
        title="Email",
        description="User's email address",
        json_schema_extra={"example": "user@example.com"}
    )
    full_name: str = Field(
        ...,
        title="Full Name",
        description="User's full name",
        min_length=2,
        max_length=100,
        json_schema_extra={"example": "John Doe"}
    )
    level: str = Field(
        ...,
        title="Academic Level",
        description="User's academic level (e.g., HND, BSc)",
        max_length=50,
        json_schema_extra={"example": "HND"}
    )
    institution: str = Field(
        ...,
        title="Institution",
        description="User's institution name",
        max_length=200,
        json_schema_extra={"example": "My University"}
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "level": "HND",
                "institution": "My University"
            }
        }
    )

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(
        ...,
        title="Password",
        description="User's password (will be hashed)",
        min_length=8,
        max_length=100,
        json_schema_extra={"example": "strongpassword123"}
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "full_name": "John Doe",
                "level": "HND",
                "institution": "My University"
            }
        }
    )

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(
        ..., 
        title="Email",
        description="User's email address",
        json_schema_extra={"example": "user@example.com"}
    )
    password: str = Field(
        ...,
        title="Password",
        description="User's password",
        min_length=8,
        json_schema_extra={"example": "strongpassword123"}
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123"
            }
        }
    )

class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str = Field(
        ...,
        title="Access Token",
        description="JWT access token"
    )
    token_type: str = Field(
        default="bearer",
        title="Token Type",
        description="Token type"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(
        None,
        title="Full Name",
        description="New full name",
        min_length=2,
        max_length=100,
        json_schema_extra={"example": "John Doe Updated"}
    )
    level: Optional[str] = Field(
        None,
        title="Academic Level",
        description="New academic level",
        max_length=50,
        json_schema_extra={"example": "BSc"}
    )
    institution: Optional[str] = Field(
        None,
        title="Institution",
        description="New institution name",
        max_length=200,
        json_schema_extra={"example": "New University"}
    )
    password: Optional[str] = Field(
        None,
        title="Password",
        description="New password (will be hashed)",
        min_length=8,
        max_length=100,
        json_schema_extra={"example": "newstrongpassword123"}
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "John Doe Updated",
                "level": "BSc",
                "institution": "New University",
                "password": "newstrongpassword123"
            }
        }
    )

class UserResponse(UserBase):
    """Schema for user response data"""
    id: UUID = Field(
        ...,
        title="User ID",
        description="User's unique identifier",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"}
    )
    is_active: bool = Field(
        ...,
        title="Active Status",
        description="Whether the user account is active",
        json_schema_extra={"example": True}
    )
    created_at: datetime = Field(
        ...,
        title="Created At",
        description="When the user account was created",
        json_schema_extra={"example": "2024-01-01T00:00:00Z"}
    )
    last_login: Optional[datetime] = Field(
        None,
        title="Last Login",
        description="When the user last logged in",
        json_schema_extra={"example": "2024-01-01T12:00:00Z"}
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "level": "HND",
                "institution": "My University",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-01T12:00:00Z"
            }
        }
    )

class UserInDB(UserResponse):
    """Schema for user in database, includes hashed password"""
    hashed_password: str = Field(
        ...,
        title="Hashed Password",
        description="User's hashed password",
        json_schema_extra={"example": "hashed_password_string"}
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "level": "HND",
                "institution": "My University",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-01T12:00:00Z",
                "hashed_password": "hashed_password_string"
            }
        }
    )