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
    """
    Generate a unique reference number for payment tracking.
    
    Returns:
        str: UUID4 string used as unique transaction identifier
        
    Note: This reference number can be used for:
    - Payment gateway integration
    - Transaction reconciliation
    - Refund processing
    - Customer support queries
    """
    return str(uuid.uuid4())

@router.post("/payments/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """
    Create a new payment record.
    
    Args:
        payment: PaymentCreate schema (booking_id, mode_of_payment, payment_maker, user_id)
        db: Database session dependency
        
    Returns:
        PaymentResponse: Created payment with auto-generated reference_no
        
    Important:
        - reference_no is automatically generated (do not include in request)
        - booking_id must exist in bookings table (foreign key constraint)
        - Each payment gets a unique reference number for transaction tracking
        
    Raises:
        HTTPException: If booking_id doesn't exist or database constraint fails
    """
    # Auto-generate unique reference number for this transaction
    reference_no = generate_reference_number()
    
    # Create payment record with generated reference number
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
