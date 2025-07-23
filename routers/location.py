from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.location_model import Location
from schemes.location import LocationCreate
from typing import List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/locations/")
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    new_location = Location(**location.dict())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location

@router.get("/locations/", response_model=List[LocationCreate])
def list_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()

@router.get("/locations/{location_id}", response_model=LocationCreate)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.location_id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.put("/locations/{location_id}", response_model=LocationCreate)
def update_location(location_id: int, location: LocationCreate, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    for key, value in location.dict().items():
        setattr(db_location, key, value)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return {"detail": "Location deleted"}