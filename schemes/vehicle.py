from pydantic import BaseModel
from typing import Literal, Optional

class VehicleCreate(BaseModel):
    vehicle_name: str
    vehicle_number: str
    vehicle_description: Optional[str] = None
    vehicle_rc: Optional[str] = None
    vehicle_condition: Optional[str] = None
    variant: Optional[Literal["petrol", "EV", "CNG"]] = None
    vehicle_type: Literal["cab", "bike", "auto", "buses"]
    vehicle_cab_type: Literal["sedan", "hatchback", "suv", "van", "luxury"]

class VehicleResponse(VehicleCreate):
    vehicle_id: int

    class Config:
        from_attributes = True