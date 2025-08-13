from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerDashboardCreate(BaseModel):
    user_id: int
    last_login: Optional[datetime] = None
    activity_summary: Optional[str] = None
    preferences: Optional[dict] = None

class CustomerDashboardResponse(CustomerDashboardCreate):
    dashboard_id: int
    class Config:
        from_attributes = True