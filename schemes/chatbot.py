from pydantic import BaseModel
from typing import Optional, Literal

class ChatMessage(BaseModel):
    message: str
    case_id: Optional[str] = None  # Optional for first message
    email: Optional[str] = None    # Optional user identifier
    phone: Optional[str] = None    # Optional user identifier

class ChatResponse(BaseModel):
    case_id: str
    response: str
    user_type: Literal["new", "existing"]
    query_type: Optional[str]
    conversation_status: Literal["active", "resolved", "pending"]
    suggestions: Optional[list[str]] = None  # Quick reply suggestions