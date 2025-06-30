from pydantic import BaseModel
from typing import Optional

class ServiceCreate(BaseModel):
    service_name: str
    description: Optional[str] = None
    provided_by: str  # e.g., 'company' or 'partner'
    partner_id: Optional[int] = None
    price: float