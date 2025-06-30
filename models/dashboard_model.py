from sqlalchemy import Column, Integer, DateTime, Text, JSON, ForeignKey
from databases.database import Base

class Dashboard(Base):
    __tablename__ = "dashboards"
    dashboard_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    last_login = Column(DateTime)
    activity_summary = Column(Text)
    preferences = Column(JSON)