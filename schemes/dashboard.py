from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class DashboardCreate(BaseModel):
    user_id: int
    last_login: Optional[datetime] = None
    activity_summary: Optional[str] = None
    preferences: Optional[Any] = None  # JSON field

class DashboardResponse(DashboardCreate):
    dashboard_id: int

    class Config:
        from_attributes = True