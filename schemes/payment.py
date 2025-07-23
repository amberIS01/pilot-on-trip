from pydantic import BaseModel
from typing import Optional

class PaymentCreate(BaseModel):
    booking_id: str
    upi_id: Optional[str] = None
    payment_maker: str
    user_id: int

class PaymentResponse(PaymentCreate):
    payment_id: int
    reference_no: str

    class Config:
        from_attributes = True
