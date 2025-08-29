from sqlalchemy import Column, Integer, String
from databases.database import Base

class Location(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=False)