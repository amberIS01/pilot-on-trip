from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.dashboard_model import Dashboard
from schemes.dashboard import DashboardCreate
from typing import List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/dashboards/")
def create_dashboard(dashboard: DashboardCreate, db: Session = Depends(get_db)):
    new_dashboard = Dashboard(**dashboard.dict())
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    return new_dashboard

@router.get("/dashboards/", response_model=List[DashboardCreate])
def list_dashboards(db: Session = Depends(get_db)):
    return db.query(Dashboard).all()

@router.get("/dashboards/{dashboard_id}", response_model=DashboardCreate)
def get_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    dashboard = db.query(Dashboard).filter(Dashboard.dashboard_id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dashboard