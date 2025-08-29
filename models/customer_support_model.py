from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from databases.database import Base
import enum
from datetime import datetime

class ServiceInterestEnum(str, enum.Enum):
    general_inquiry = "general inquiry"
    technical_support = "technical support"
    booking_issue = "booking issue"
    other = "other"

class QueryStatusEnum(str, enum.Enum):
    open = "open"
    in_progress = "in progress"
    resolved = "resolved"

class CustomerSupport(Base):
    __tablename__ = "customer_support"
    support_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    business_email = Column(String(100))
    contact_number = Column(String(20), nullable=False)
    service_interest = Column(Enum(ServiceInterestEnum), nullable=False)
    message = Column(Text)
    query_status = Column(Enum(QueryStatusEnum), default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    reference_number = Column(String(20), unique=True, nullable=False)