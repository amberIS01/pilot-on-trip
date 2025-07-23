from sqlalchemy import Column, Integer, String, ForeignKey
from databases.database import Base

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(String(36), ForeignKey("bookings.booking_id"), nullable=False)
    reference_no = Column(String(20), unique=True, nullable=False)  # Auto-generated
    upi_id = Column(String(100), nullable=True)
    payment_maker = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
