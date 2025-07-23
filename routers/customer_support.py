from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.customer_support_model import CustomerSupport
from schemes.customer_support import CustomerSupportCreate, CustomerSupportResponse
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_reference_number():
    return str(uuid.uuid4())[:8].upper()

@router.post("/customer-support/", response_model=CustomerSupportResponse)
def create_customer_support(support: CustomerSupportCreate, db: Session = Depends(get_db)):
    reference_number = generate_reference_number()
    new_support = CustomerSupport(**support.dict(), reference_number=reference_number)
    db.add(new_support)
    db.commit()
    db.refresh(new_support)
    return new_support

@router.get("/customer-support/search/{reference_number}", response_model=CustomerSupportResponse)
def search_customer_support(reference_number: str, db: Session = Depends(get_db)):
    support = db.query(CustomerSupport).filter(CustomerSupport.reference_number == reference_number).first()
    if not support:
        raise HTTPException(status_code=404, detail="Reference number not found")
    return support

# DELETE endpoint for customer_support by support_id
@router.delete("/customer-support/{support_id}")
def delete_customer_support(support_id: int, db: Session = Depends(get_db)):
    support = db.query(CustomerSupport).filter(CustomerSupport.support_id == support_id).first()
    if not support:
        raise HTTPException(status_code=404, detail="Customer support entry not found")
    db.delete(support)
    db.commit()
    return {"detail": "Customer support entry deleted successfully"}