from sqlalchemy import Column, Integer, String, Enum
from databases.database import Base
import enum

class PartnerTypeEnum(str, enum.Enum):
    individual = "individual"
    multiple_user = "multiple user"

class PartnerQuery(Base):
    __tablename__ = "partner_query"
    query_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    partner_type = Column(Enum(PartnerTypeEnum), nullable=False)
    full_name = Column(String(100), nullable=False)
    contact_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    nation = Column(String(100), nullable=False)
    current_location = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    subject = Column(String(255), nullable=False)
    reference_number = Column(String(20), unique=True, nullable=False)

