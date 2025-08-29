from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RiderDashboardCreate(BaseModel):
    rider_id: int
    partner_id: Optional[int] = None
    booking_location: str
    destination_location: str
    duration: Optional[int] = None
    user_name: Optional[str] = None
    user_uuid: Optional[str] = None
    partner_name: Optional[str] = None
    partner_size: Optional[int] = None
    created_at: Optional[datetime] = None

class RiderDashboardResponse(RiderDashboardCreate):
    rider_dashboard_id: int
    class Config:
        from_attributes = True
