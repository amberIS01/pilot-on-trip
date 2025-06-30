from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: str
    location_id: Optional[int] = None
    profile_photo: Optional[str] = None
    vehicle_id: Optional[int] = None
    partner_id: Optional[int] = None

class UserResponse(UserCreate):
    user_id: int
    created_at: datetime