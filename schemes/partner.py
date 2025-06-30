from pydantic import BaseModel
from typing import Literal, Optional

class PartnerCreate(BaseModel):
    user_id: int
    partner_type: Literal["individual", "multiple user"]
    company_name: Optional[str] = None
    company_size: Optional[int] = None