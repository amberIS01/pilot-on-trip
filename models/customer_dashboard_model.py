from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from databases.database import Base
from datetime import datetime

class CustomerDashboard(Base):
    __tablename__ = "customer_dashboards"
    dashboard_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    last_login = Column(DateTime, nullable=True)
    activity_summary = Column(Text, nullable=True)
    booking_id = Column(String(36), ForeignKey("bookings.booking_id"), nullable=True)  # UUID reference