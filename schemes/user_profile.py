from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

class UserProfileCreate(BaseModel):
    # Optional user info - can be filled during conversation
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    
    # Conversation info
    user_type: Optional[Literal["new", "existing"]] = "new"
    query_type: Optional[str] = None  # booking, support, general
    
    # Initial message
    last_message: Optional[str] = None

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    user_type: Optional[Literal["new", "existing"]] = None
    query_type: Optional[str] = None
    conversation_status: Optional[Literal["active", "resolved", "pending"]] = None
    last_message: Optional[str] = None
    conversation_summary: Optional[str] = None

class UserProfileResponse(BaseModel):
    case_id: str
    user_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    user_type: Literal["new", "existing"]
    query_type: Optional[str]
    conversation_status: Literal["active", "resolved", "pending"]
    last_message: Optional[str]
    conversation_summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True