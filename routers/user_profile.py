from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.user_profile_model import UserProfile
from schemes.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from typing import List
import random
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_case_id(db: Session) -> str:
    """Generate unique case ID in format CASE000001"""
    while True:
        case_number = random.randint(1, 999999)
        case_id = f"CASE{case_number:06d}"
        existing = db.query(UserProfile).filter(UserProfile.case_id == case_id).first()
        if not existing:
            return case_id

@router.post("/user_profiles/", response_model=UserProfileResponse)
def create_user_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    # Check for existing user by email or phone if provided
    if profile.email or profile.phone:
        existing_conditions = []
        if profile.email:
            existing_conditions.append(UserProfile.email == profile.email)
        if profile.phone:
            existing_conditions.append(UserProfile.phone == profile.phone)
        
        if existing_conditions:
            db_profile = db.query(UserProfile).filter(
                *existing_conditions
            ).first()
            if db_profile:
                # Update user_type to existing if user found
                profile.user_type = "existing"
    
    # Generate case ID
    case_id = generate_case_id(db)
    
    # Create new profile with case ID
    new_profile = UserProfile(
        case_id=case_id,
        **profile.dict()
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/user_profiles/", response_model=List[UserProfileResponse])
def list_user_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = db.query(UserProfile).offset(skip).limit(limit).all()
    return profiles

@router.get("/user_profiles/{case_id}", response_model=UserProfileResponse)
def get_user_profile(case_id: str, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.case_id == case_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Case not found")
    return profile

@router.get("/user_profiles/active-cases/", response_model=List[UserProfileResponse])
def get_active_cases(db: Session = Depends(get_db)):
    profiles = db.query(UserProfile).filter(UserProfile.conversation_status == "active").all()
    return profiles

@router.put("/user_profiles/{case_id}", response_model=UserProfileResponse)
def update_user_profile(case_id: str, profile_update: UserProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.case_id == case_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Case not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/user_profiles/{case_id}")
def delete_user_profile(case_id: str, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.case_id == case_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Case not found")
    
    db.delete(profile)
    db.commit()
    return {"message": "User profile deleted successfully"}