from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole
    is_active: bool
    is_verified: bool
    agency_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None

class FreelancerProfileUpdate(BaseModel):
    bio: Optional[str] = None
    hourly_rate: Optional[float] = None
    experience_years: Optional[int] = None
    is_available: Optional[bool] = None

class FreelancerProfileResponse(BaseModel):
    id: int
    user_id: int
    bio: Optional[str]
    hourly_rate: Optional[float]
    experience_years: int
    average_rating: float
    is_available: bool

    class Config:
        from_attributes = True