from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal

class BookingCreate(BaseModel):
    booking_details: Optional[str] = None
    vehicle_number: Optional[str] = None
    vehicle_type: Optional[Literal["cab", "auto", "bike", "buses"]] = None
    pickup_location: str
    vehicle_variant_type: Optional[Literal["petrol", "EV", "CNG"]] = None
    language: Optional[str] = None
    drop_location: str
    booking_schedule: datetime
    number_of_person: int
    rider_id: Optional[int] = None
    booking_price: Decimal

class BookingResponse(BookingCreate):
    booking_id: str
    time_of_booking: datetime

    class Config:
        from_attributes = True
