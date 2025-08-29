from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminDashboardCreate(BaseModel):
    vehicle_id: int
    rider_id: int
    created_at: Optional[datetime] = None

class AdminDashboardResponse(AdminDashboardCreate):
    admin_dashboard_id: int
    class Config:
        from_attributes = True
