from sqlalchemy import Column, Integer, String, Enum
from databases.database import Base
import enum

class VehicleTypeEnum(str, enum.Enum):
    cab = "cab"
    bike = "bike"
    auto = "auto"

class VehicleCabTypeEnum(str, enum.Enum):
    sedan = "sedan"
    hatchback = "hatchback"
    suv = "suv"
    van = "van"
    luxury = "luxury"

class Vehicle(Base):
    __tablename__ = "vehicle"
    vehicle_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_name = Column(String(50), nullable=False)
    vehicle_number = Column(Integer, nullable=False)
    vehicle_description = Column(String(200))
    vehicle_type = Column(Enum(VehicleTypeEnum), nullable=False)
    vehicle_cab_type = Column(Enum(VehicleCabTypeEnum), nullable=False)