from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.rider_dashboard_model import RiderDashboard
from schemes.rider_dashboard import RiderDashboardCreate, RiderDashboardResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/rider_dashboard/", response_model=RiderDashboardResponse)
def create_rider_dashboard(dashboard: RiderDashboardCreate, db: Session = Depends(get_db)):
    new_dashboard = RiderDashboard(**dashboard.dict())
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    return new_dashboard

@router.get("/rider_dashboard/", response_model=List[RiderDashboardResponse])
def list_rider_dashboards(db: Session = Depends(get_db)):
    return db.query(RiderDashboard).all()

@router.get("/rider_dashboard/{rider_dashboard_id}", response_model=RiderDashboardResponse)
def get_rider_dashboard(rider_dashboard_id: int, db: Session = Depends(get_db)):
    dashboard = db.query(RiderDashboard).filter(RiderDashboard.rider_dashboard_id == rider_dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Rider Dashboard not found")
    return dashboard

@router.put("/rider_dashboard/{rider_dashboard_id}", response_model=RiderDashboardResponse)
def update_rider_dashboard(rider_dashboard_id: int, dashboard: RiderDashboardCreate, db: Session = Depends(get_db)):
    db_dashboard = db.query(RiderDashboard).filter(RiderDashboard.rider_dashboard_id == rider_dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Rider Dashboard not found")
    for key, value in dashboard.dict().items():
        setattr(db_dashboard, key, value)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

@router.delete("/rider_dashboard/{rider_dashboard_id}")
def delete_rider_dashboard(rider_dashboard_id: int, db: Session = Depends(get_db)):
    db_dashboard = db.query(RiderDashboard).filter(RiderDashboard.rider_dashboard_id == rider_dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Rider Dashboard not found")
    db.delete(db_dashboard)
    db.commit()
    return {"detail": "Rider Dashboard deleted"}
