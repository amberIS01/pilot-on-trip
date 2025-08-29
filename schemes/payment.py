from pydantic import BaseModel
from typing import Literal

class PaymentCreate(BaseModel):
    booking_id: str
    mode_of_payment: Literal["upi", "netbanking", "cash", "card"]
    payment_maker: str
    user_id: int

class PaymentResponse(PaymentCreate):
    payment_id: int
    reference_no: str  # UUID auto-generated

    class Config:
        from_attributes = True
