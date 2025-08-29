from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.rider_model import Rider
from schemes.rider import RiderCreate, RiderResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/rider/", response_model=RiderResponse)
def create_rider(rider: RiderCreate, db: Session = Depends(get_db)):
    new_rider = Rider(**rider.dict())
    db.add(new_rider)
    db.commit()
    db.refresh(new_rider)
    return new_rider

@router.get("/rider/", response_model=list[RiderResponse])
def list_riders(db: Session = Depends(get_db)):
    return db.query(Rider).all()

@router.get("/rider/{rider_id}", response_model=RiderResponse)
def get_rider(rider_id: int, db: Session = Depends(get_db)):
    rider = db.query(Rider).filter(Rider.rider_id == rider_id).first()
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return rider

@router.put("/rider/{rider_id}", response_model=RiderResponse)
def update_rider(rider_id: int, rider: RiderCreate, db: Session = Depends(get_db)):
    db_rider = db.query(Rider).filter(Rider.rider_id == rider_id).first()
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    for key, value in rider.dict(exclude_unset=True).items():
        setattr(db_rider, key, value)
    db.commit()
    db.refresh(db_rider)
    return db_rider

@router.delete("/rider/{rider_id}")
def delete_rider(rider_id: int, db: Session = Depends(get_db)):
    db_rider = db.query(Rider).filter(Rider.rider_id == rider_id).first()
    if not db_rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    db.delete(db_rider)
    db.commit()
    return {"detail": "Rider deleted successfully"}
