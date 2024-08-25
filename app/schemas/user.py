# Pydantic models for user-related data validation and serialization.

from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[UserRole]= UserRole.user

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True