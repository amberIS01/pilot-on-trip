from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.payment_model import Payment
from schemes.payment import PaymentCreate, PaymentResponse
from typing import List
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_reference_number():
    return str(uuid.uuid4())[:10].upper()

@router.post("/payments/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    reference_no = generate_reference_number()
    new_payment = Payment(**payment.dict(), reference_no=reference_no)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/payments/", response_model=List[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()

@router.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/payments/booking/{booking_id}", response_model=List[PaymentResponse])
def get_payments_by_booking(booking_id: str, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.booking_id == booking_id).all()
    return payments

@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"detail": "Payment deleted successfully"}
