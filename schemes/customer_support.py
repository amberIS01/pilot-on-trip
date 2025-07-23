from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

class CustomerSupportCreate(BaseModel):
    full_name: str
    business_email: Optional[EmailStr] = None
    contact_number: str
    service_interest: Literal["general inquiry", "technical support", "booking issue", "other"]
    message: Optional[str] = None

class CustomerSupportResponse(CustomerSupportCreate):
    support_id: int
    query_status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    reference_number: str

    class Config:
        from_attributes = True
