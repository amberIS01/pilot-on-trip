from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from databases.database import Base
from datetime import datetime

class RiderDashboard(Base):
    __tablename__ = "rider_dashboard"
    rider_dashboard_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rider_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), nullable=True)
    booking_location = Column(String(100), nullable=True)
    destination_location = Column(String(100), nullable=True)
    duration = Column(Integer, nullable=True)
    user_name = Column(String(100), nullable=True)
    user_uuid = Column(String(36), nullable=True)
    partner_name = Column(String(100), nullable=True)
    partner_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
