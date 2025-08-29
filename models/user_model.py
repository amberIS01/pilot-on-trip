from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from databases.database import Base
import enum
from datetime import datetime

class UserTypeEnum(str, enum.Enum):
    partner = "partner"
    customer = "customer"

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    partner_id = Column(Integer, ForeignKey("partners.partner_id"), nullable=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    preferred_language = Column(String(50), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"), nullable=True)
    profile_photo = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    vehicle_id = Column(Integer, ForeignKey("vehicle.vehicle_id"), nullable=True)