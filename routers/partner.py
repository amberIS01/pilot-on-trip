from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.partner_model import Partner
from schemes.partner import PartnerCreate, PartnerResponse
from typing import List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/partners/", response_model=PartnerResponse)
def create_partner(partner: PartnerCreate, db: Session = Depends(get_db)):
    new_partner = Partner(**partner.dict())
    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)
    return new_partner


@router.get("/partners/", response_model=List[PartnerResponse])
def list_partners(db: Session = Depends(get_db)):
    return db.query(Partner).all()


@router.get("/partners/{partner_id}", response_model=PartnerResponse)
def get_partner(partner_id: int, db: Session = Depends(get_db)):
    partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner


@router.put("/partners/{partner_id}", response_model=PartnerResponse)
def update_partner(partner_id: int, partner: PartnerCreate, db: Session = Depends(get_db)):
    db_partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    for key, value in partner.dict().items():
        setattr(db_partner, key, value)
    db.commit()
    db.refresh(db_partner)
    return db_partner

@router.delete("/partners/{partner_id}")
def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    db_partner = db.query(Partner).filter(Partner.partner_id == partner_id).first()
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    db.delete(db_partner)
    db.commit()
    return {"detail": "Partner deleted"}