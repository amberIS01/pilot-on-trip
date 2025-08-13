from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from databases.database import Base
import enum

class PartnerTypeEnum(str, enum.Enum):
    individual = "individual"
    multiple_user = "multiple user"

class Partner(Base):
    __tablename__ = "partners"
    partner_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number_of_users = Column(Integer, nullable=True)
    rider_id = Column(Integer, nullable=True)  # Should be ForeignKey if Rider table exists
    partners_role = Column(String(100), nullable=True)  # ENUM not specified, using String
    user_id = Column(Integer, ForeignKey("users.user_id"))
    partner_type = Column(Enum(PartnerTypeEnum), nullable=False)
    company_name = Column(String(255))
    company_size = Column(Integer)
    aadhare_card_number = Column(String(50), nullable=True)
    pan_card = Column(String(50), nullable=True)
    partner_rating = Column(Integer, default=0)  # Feedback rating (0-4)