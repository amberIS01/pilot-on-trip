from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.partner_query_model import PartnerQuery
from schemes.partner_query import PartnerQueryCreate, PartnerQueryResponse
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

@router.post("/partner-query/", response_model=PartnerQueryResponse)
def create_partner_query(query: PartnerQueryCreate, db: Session = Depends(get_db)):
    reference_number = generate_reference_number()
    new_query = PartnerQuery(**query.dict(), reference_number=reference_number)
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

@router.get("/partner-query/search/{reference_number}", response_model=PartnerQueryResponse)
def search_partner_query(reference_number: str, db: Session = Depends(get_db)):
    query = db.query(PartnerQuery).filter(PartnerQuery.reference_number == reference_number).first()
    if not query:
        raise HTTPException(status_code=404, detail="Reference number not found")
    return query

# DELETE endpoint for partner_query by query_id
@router.delete("/partner-query/{query_id}")
def delete_partner_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(PartnerQuery).filter(PartnerQuery.query_id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Partner query not found")
    db.delete(query)
    db.commit()
    return {"detail": "Partner query deleted successfully"}