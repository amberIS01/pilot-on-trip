from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    rider_id: int
    user_id: int
    pickup_location: str
    destination: str
    rating: int
    feedback: Optional[str] = None
    created_at: Optional[datetime] = None

class FeedbackResponse(FeedbackCreate):
    ride_id: int
    class Config:
        from_attributes = True
