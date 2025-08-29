from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerDashboardCreate(BaseModel):
    user_id: int
    last_login: Optional[datetime] = None
    activity_summary: Optional[str] = None
    booking_id: Optional[str] = None  # UUID reference to bookings table

class CustomerDashboardUpdate(BaseModel):
    last_login: Optional[datetime] = None
    activity_summary: Optional[str] = None
    booking_id: Optional[str] = None

class CustomerDashboardResponse(CustomerDashboardCreate):
    dashboard_id: int
    
    class Config:
        from_attributes = True