from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.service_model import Service
from schemes.service import ServiceCreate
from typing import List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/services/")
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new_service = Service(**service.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.get("/services/", response_model=List[ServiceCreate])
def list_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

@router.get("/services/{service_id}", response_model=ServiceCreate)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.service_id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/services/{service_id}", response_model=ServiceCreate)
def update_service(service_id: int, service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.service_id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    for key, value in service.dict().items():
        setattr(db_service, key, value)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.service_id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(db_service)
    db.commit()
    return {"detail": "Service deleted"}