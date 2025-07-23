from pydantic import BaseModel
from typing import Optional

class RiderCreate(BaseModel):
    rider_name: str
    current_address: Optional[str] = None
    nationality: Optional[str] = None
    rider_city: Optional[str] = None
    rider_state: Optional[str] = None
    rider_age: Optional[int] = None
    pan_card: Optional[str] = None
    rider_language: Optional[str] = None

class RiderResponse(RiderCreate):
    rider_id: int

    class Config:
        from_attributes = True
