from sqlalchemy import Column, Integer, String
from databases.database import Base

class Rider(Base):
    __tablename__ = "rider"
    rider_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rider_name = Column(String(20), nullable=False)
    current_address = Column(String(200), nullable=True)
    nationality = Column(String(50), nullable=True)
    rider_city = Column(String(50), nullable=True)
    rider_state = Column(String(50), nullable=True)
    rider_age = Column(Integer, nullable=True)
    pan_card = Column(String(50), nullable=True)
    rider_language = Column(String(50), nullable=True)
