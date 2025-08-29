from pydantic import BaseModel

class LocationCreate(BaseModel):
    city: str
    state: str
    country: str
    pincode: str

class LocationResponse(LocationCreate):
    location_id: int

    class Config:
        from_attributes = True