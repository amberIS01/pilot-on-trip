from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.feedback_model import Feedback
from schemes.feedback import FeedbackCreate, FeedbackResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback/", response_model=FeedbackResponse)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    new_feedback = Feedback(**feedback.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

@router.get("/feedback/", response_model=List[FeedbackResponse])
def list_feedbacks(db: Session = Depends(get_db)):
    return db.query(Feedback).all()

@router.get("/feedback/{ride_id}", response_model=FeedbackResponse)
def get_feedback(ride_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.ride_id == ride_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.put("/feedback/{ride_id}", response_model=FeedbackResponse)
def update_feedback(ride_id: int, feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.ride_id == ride_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    for key, value in feedback.dict().items():
        setattr(db_feedback, key, value)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.delete("/feedback/{ride_id}")
def delete_feedback(ride_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.ride_id == ride_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(db_feedback)
    db.commit()
    return {"detail": "Feedback deleted"}
