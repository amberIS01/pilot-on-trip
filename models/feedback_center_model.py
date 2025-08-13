from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Text
from databases.database import Base
from datetime import datetime
import enum

class FeedbackTypeEnum(str, enum.Enum):
    partner = "partner"
    rider = "rider"
    platform = "platform"

class FeedbackCenter(Base):
    __tablename__ = "feedback_center"
    feedback_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feedback_type = Column(Enum(FeedbackTypeEnum), nullable=False)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), nullable=True)
    rider_id = Column(Integer, ForeignKey("rider.rider_id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer, nullable=False)  # Scale 0–4
    feedback_text = Column(Text, nullable=True)
    ticket_code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
