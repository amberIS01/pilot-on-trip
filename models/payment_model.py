from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from databases.database import Base
import enum

class PaymentModeEnum(str, enum.Enum):
    upi = "upi"
    netbanking = "netbanking"
    cash = "cash"
    card = "card"

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(String(36), ForeignKey("bookings.booking_id"), nullable=False)
    reference_no = Column(String(36), unique=True, nullable=False)  # UUID format
    mode_of_payment = Column(Enum(PaymentModeEnum), nullable=False)
    payment_maker = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
