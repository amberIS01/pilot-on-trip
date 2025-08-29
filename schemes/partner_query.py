from pydantic import BaseModel, EmailStr
from typing import Literal

class PartnerQueryCreate(BaseModel):
    partner_type: Literal["individual", "multiple"]
    full_name: str
    contact_number: str
    email: EmailStr
    nation: str
    current_location: str
    state: str
    city: str
    subject: str

class PartnerQueryResponse(PartnerQueryCreate):
    query_id: int
    reference_number: str

    class Config:
        from_attributes = True
