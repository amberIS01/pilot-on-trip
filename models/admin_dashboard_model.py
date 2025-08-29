from sqlalchemy import Column, Integer, DateTime, ForeignKey
from databases.database import Base
from datetime import datetime

class AdminDashboard(Base):
    __tablename__ = "admin_dashboard"
    admin_dashboard_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_id = Column(Integer, ForeignKey("vehicle.vehicle_id"), nullable=False)
    rider_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
