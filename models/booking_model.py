from sqlalchemy import Column, String, Text, Integer, DateTime, Enum, ForeignKey, DECIMAL
from databases.database import Base
from datetime import datetime
import enum

class VehicleTypeEnum(str, enum.Enum):
    cab = "cab"
    auto = "auto"
    bike = "bike"
    buses = "buses"

class VehicleVariantEnum(str, enum.Enum):
    petrol = "petrol"
    ev = "EV"
    cng = "CNG"

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(String(36), primary_key=True, index=True)  # UUID
    booking_details = Column(Text, nullable=True)
    vehicle_number = Column(String(50), nullable=True)
    vehicle_type = Column(Enum(VehicleTypeEnum), nullable=True)
    pickup_location = Column(String(200), nullable=False)
    vehicle_variant_type = Column(Enum(VehicleVariantEnum), nullable=True)
    language = Column(String(50), nullable=True)
    drop_location = Column(String(200), nullable=False)
    booking_schedule = Column(DateTime, nullable=False)
    time_of_booking = Column(DateTime, default=datetime.utcnow)
    number_of_person = Column(Integer, nullable=False)
    rider_id = Column(Integer, ForeignKey("rider.rider_id"), nullable=True)
    booking_price = Column(DECIMAL(10,2), nullable=False)
