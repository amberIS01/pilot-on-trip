from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.booking_model import Booking
from schemes.booking import BookingCreate, BookingResponse
from typing import List
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_booking_id():
    return str(uuid.uuid4())

@router.post("/bookings/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    booking_id = generate_booking_id()
    new_booking = Booking(**booking.dict(), booking_id=booking_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/bookings/", response_model=List[BookingResponse])
def list_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@router.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: str, booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    for key, value in booking.dict().items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.delete("/bookings/{booking_id}")
def delete_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"detail": "Booking deleted successfully"}
