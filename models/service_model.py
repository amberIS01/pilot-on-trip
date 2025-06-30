from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from databases.database import Base

class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_name = Column(String(100), nullable=False)
    description = Column(Text)
    provided_by = Column(String(20), nullable=False)  # 'company', 'partner'
    partner_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)