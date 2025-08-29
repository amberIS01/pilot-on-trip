from pydantic import BaseModel
from typing import Literal, Optional


class PartnerCreate(BaseModel):
    user_id: int
    partner_type: Literal["individual", "multiple user"]
    company_name: Optional[str] = None
    company_size: Optional[int] = None
    number_of_users: Optional[int] = None
    rider_id: Optional[int] = None
    partners_role: Optional[str] = None
    aadhare_card_number: Optional[str] = None
    pan_card: Optional[str] = None

class PartnerResponse(PartnerCreate):
    partner_id: int

    class Config:
        from_attributes = True