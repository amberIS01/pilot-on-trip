from pydantic import BaseModel
from typing import Literal

class VehicleCreate(BaseModel):
    vehicle_name: str
    vehicle_number: int
    vehicle_description: str
    vehicle_type: Literal["cab", "bike", "auto"]
    vehicle_cab_type: Literal["sedan", "hatchback", "suv", "van", "luxury"]

class VehicleResponse(VehicleCreate):
    vehicle_id: int

    class Config:
        from_attributes = True