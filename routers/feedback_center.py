from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.feedback_center_model import FeedbackCenter
from schemes.feedback_center import FeedbackCenterCreate, FeedbackCenterResponse
from typing import List
import random
import string

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_ticket_code(db: Session) -> str:
    prefix = "PILOT"
    while True:
        random_number = ''.join(random.choices(string.digits, k=7))
        ticket_code = prefix + random_number
        existing = db.query(FeedbackCenter).filter_by(ticket_code=ticket_code).first()
        if not existing:
            return ticket_code

@router.post("/feedback_center/", response_model=FeedbackCenterResponse)
def create_feedback_center(feedback: FeedbackCenterCreate, db: Session = Depends(get_db)):
    ticket_code = generate_ticket_code(db)
    new_feedback = FeedbackCenter(**feedback.dict(), ticket_code=ticket_code)
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

@router.get("/feedback_center/", response_model=List[FeedbackCenterResponse])
def list_feedback_centers(db: Session = Depends(get_db)):
    return db.query(FeedbackCenter).all()

@router.get("/feedback_center/{feedback_id}", response_model=FeedbackCenterResponse)
def get_feedback_center(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(FeedbackCenter).filter(FeedbackCenter.feedback_id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback Center entry not found")
    return feedback

@router.delete("/feedback_center/{feedback_id}")
def delete_feedback_center(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(FeedbackCenter).filter(FeedbackCenter.feedback_id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback Center entry not found")
    db.delete(feedback)
    db.commit()
    return {"detail": "Feedback Center entry deleted"}
