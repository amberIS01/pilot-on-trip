from sqlalchemy import Column, String, DateTime, Enum, Text
from databases.database import Base
from datetime import datetime
import enum
import uuid

class UserTypeEnum(str, enum.Enum):
    new = "new"
    existing = "existing"

class ConversationStatusEnum(str, enum.Enum):
    active = "active"
    resolved = "resolved"
    pending = "pending"

class UserProfile(Base):
    __tablename__ = "user_profile"
    case_id = Column(String(20), primary_key=True)  # CASE001234 format
    user_id = Column(String(36), nullable=True, default=lambda: str(uuid.uuid4()))
    
    # Basic user info (optional - filled during conversation)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=True)
    
    # Conversation tracking
    user_type = Column(Enum(UserTypeEnum), default=UserTypeEnum.new)
    query_type = Column(String(100), nullable=True)  # booking, support, general, etc.
    conversation_status = Column(Enum(ConversationStatusEnum), default=ConversationStatusEnum.active)
    
    # Assistant data
    last_message = Column(Text, nullable=True)
    conversation_summary = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)