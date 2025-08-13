from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from databases.database import Base
from datetime import datetime

class Feedback(Base):
    __tablename__ = "ride_feedback"
    ride_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rider_id = Column(Integer, ForeignKey("rider.rider_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    pickup_location = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)
    rating = Column(Integer, nullable=False)  # Scale 0–4
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
