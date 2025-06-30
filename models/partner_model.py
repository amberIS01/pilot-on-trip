from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from databases.database import Base
import enum

class PartnerTypeEnum(str, enum.Enum):
    individual = "individual"
    multiple_user = "multiple user"

class Partner(Base):
    __tablename__ = "partners"
    partner_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    partner_type = Column(Enum(PartnerTypeEnum), nullable=False)
    company_name = Column(String(255))
    company_size = Column(Integer)