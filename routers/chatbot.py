from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.user_profile_model import UserProfile
from schemes.chatbot import ChatMessage, ChatResponse
from datetime import datetime
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_case_id(db: Session) -> str:
    """Generate unique case ID"""
    while True:
        case_number = random.randint(1, 999999)
        case_id = f"CASE{case_number:06d}"
        existing = db.query(UserProfile).filter(UserProfile.case_id == case_id).first()
        if not existing:
            return case_id

def detect_query_type(message: str) -> str:
    """Simple keyword-based query type detection"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["book", "ride", "cab", "pickup", "driver"]):
        return "booking"
    elif any(word in message_lower for word in ["problem", "issue", "complaint", "help", "support"]):
        return "support"
    elif any(word in message_lower for word in ["payment", "refund", "bill", "charge"]):
        return "payment"
    elif any(word in message_lower for word in ["price", "cost", "rate", "fare"]):
        return "pricing"
    else:
        return "general"

def generate_response(query_type: str, user_type: str, message: str, user_profile: UserProfile = None) -> tuple[str, list[str]]:
    """Generate appropriate response based on query type and context"""
    
    suggestions = []
    
    # Extract name from message if user says "My name is..."
    message_lower = message.lower()
    if "my name is" in message_lower:
        name_start = message_lower.index("my name is") + 11
        potential_name = message[name_start:].strip().split()[0] if message[name_start:].strip() else ""
        if potential_name and user_profile:
            user_profile.name = potential_name.capitalize()
    
    # Extract phone from message
    import re
    phone_match = re.search(r'\b\d{10}\b', message)
    if phone_match and user_profile and not user_profile.phone:
        user_profile.phone = phone_match.group()
    
    # Welcome messages for new users
    if user_type == "new" and not user_profile.name:
        response = "Welcome to PilotsOnTip! I'm your assistant. May I know your name?"
        suggestions = ["Book a ride", "Check prices", "Get support"]
        return response, suggestions
    
    # Responses based on query type
    if query_type == "booking":
        if not user_profile.name:
            response = "I'll help you book a ride. First, may I have your name?"
            suggestions = ["Book a ride", "Check prices", "Get support"]
        elif not user_profile.phone:
            response = f"Thanks {user_profile.name}! Please provide your phone number for booking confirmation."
            suggestions = ["Continue booking", "Cancel"]
        else:
            response = f"Great {user_profile.name}! Where would you like to be picked up from?"
            suggestions = ["Current location", "Enter address", "Airport", "Railway station"]
    
    elif query_type == "support":
        response = "I understand you need assistance. Can you please describe your issue in detail?"
        if user_profile.name:
            response = f"Hi {user_profile.name}, " + response
        suggestions = ["Booking issue", "Payment problem", "Driver complaint", "Other"]
    
    elif query_type == "payment":
        response = "I'll help you with payment-related queries. What specific information do you need?"
        suggestions = ["Check fare", "Payment methods", "Refund status", "Transaction history"]
    
    elif query_type == "pricing":
        response = "Our pricing varies by vehicle type:\n• Bike: $10/km\n• Auto: $15/km\n• Cab: $20/km\n• SUV: $30/km"
        suggestions = ["Book now", "Calculate fare", "View all vehicles"]
    
    else:
        if user_type == "existing":
            response = f"Welcome back{' ' + user_profile.name if user_profile.name else ''}! How can I assist you today?"
        else:
            response = "Hello! How can I help you today?"
        suggestions = ["Book a ride", "Track booking", "Get support", "Check prices"]
    
    return response, suggestions

@router.post("/chat/", response_model=ChatResponse)
def chat_with_assistant(chat: ChatMessage, db: Session = Depends(get_db)):
    """Main chat endpoint for the AI assistant"""
    
    user_profile = None
    user_type = "new"
    
    # If case_id provided, retrieve existing conversation
    if chat.case_id:
        user_profile = db.query(UserProfile).filter(UserProfile.case_id == chat.case_id).first()
        if not user_profile:
            raise HTTPException(status_code=404, detail="Case not found")
    
    # Check if existing user by email or phone
    if not user_profile and (chat.email or chat.phone):
        if chat.email:
            existing = db.query(UserProfile).filter(UserProfile.email == chat.email).first()
            if existing:
                user_type = "existing"
        if chat.phone and not existing:
            existing = db.query(UserProfile).filter(UserProfile.phone == chat.phone).first()
            if existing:
                user_type = "existing"
    
    # Detect query type from message
    query_type = detect_query_type(chat.message)
    
    # Create new profile if needed
    if not user_profile:
        case_id = generate_case_id(db)
        user_profile = UserProfile(
            case_id=case_id,
            email=chat.email,
            phone=chat.phone,
            user_type=user_type,
            query_type=query_type,
            last_message=chat.message,
            conversation_status="active"
        )
        db.add(user_profile)
    else:
        # Update existing profile
        user_profile.last_message = chat.message
        user_profile.updated_at = datetime.utcnow()
        if chat.email and not user_profile.email:
            user_profile.email = chat.email
        if chat.phone and not user_profile.phone:
            user_profile.phone = chat.phone
    
    # Generate response (this may update user_profile.name or phone)
    response_text, suggestions = generate_response(query_type, user_type, chat.message, user_profile)
    
    # Update conversation summary
    if user_profile.conversation_summary:
        user_profile.conversation_summary += f"\nUser: {chat.message}\nBot: {response_text}"
    else:
        user_profile.conversation_summary = f"User: {chat.message}\nBot: {response_text}"
    
    # Commit changes including any name/phone updates from generate_response
    db.commit()
    db.refresh(user_profile)
    
    return ChatResponse(
        case_id=user_profile.case_id,
        response=response_text,
        user_type=user_profile.user_type,
        query_type=query_type,
        conversation_status=user_profile.conversation_status,
        suggestions=suggestions
    )

@router.get("/chat/{case_id}/history")
def get_chat_history(case_id: str, db: Session = Depends(get_db)):
    """Get conversation history for a case"""
    user_profile = db.query(UserProfile).filter(UserProfile.case_id == case_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return {
        "case_id": case_id,
        "user_type": user_profile.user_type,
        "query_type": user_profile.query_type,
        "status": user_profile.conversation_status,
        "conversation": user_profile.conversation_summary,
        "created_at": user_profile.created_at,
        "updated_at": user_profile.updated_at
    }

@router.put("/chat/{case_id}/close")
def close_conversation(case_id: str, db: Session = Depends(get_db)):
    """Mark a conversation as resolved"""
    user_profile = db.query(UserProfile).filter(UserProfile.case_id == case_id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="Case not found")
    
    user_profile.conversation_status = "resolved"
    user_profile.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"Case {case_id} marked as resolved"}