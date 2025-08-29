from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class FeedbackTypeEnum(str, Enum):
    partner = "partner"
    rider = "rider"
    platform = "platform"

class FeedbackCenterCreate(BaseModel):
    feedback_type: FeedbackTypeEnum
    partner_id: Optional[int] = None
    rider_id: Optional[int] = None
    user_id: int
    rating: int
    feedback_text: Optional[str] = None

class FeedbackCenterResponse(FeedbackCenterCreate):
    feedback_id: int
    ticket_code: str
    created_at: datetime
    class Config:
        from_attributes = True
