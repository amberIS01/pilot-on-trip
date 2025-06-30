from pydantic import BaseModel

class LocationCreate(BaseModel):
    city: str
    state: str
    country: str
    pincode: str