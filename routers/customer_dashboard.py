from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.customer_dashboard_model import CustomerDashboard
from schemes.customer_dashboard import CustomerDashboardCreate, CustomerDashboardResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/customer_dashboard/", response_model=CustomerDashboardResponse)
def create_customer_dashboard(dashboard: CustomerDashboardCreate, db: Session = Depends(get_db)):
    new_dashboard = CustomerDashboard(**dashboard.dict())
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    return new_dashboard

@router.get("/customer_dashboard/", response_model=List[CustomerDashboardResponse])
def list_customer_dashboards(db: Session = Depends(get_db)):
    return db.query(CustomerDashboard).all()

@router.get("/customer_dashboard/{dashboard_id}", response_model=CustomerDashboardResponse)
def get_customer_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.dashboard_id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found")
    return dashboard

@router.put("/customer_dashboard/{dashboard_id}", response_model=CustomerDashboardResponse)
def update_customer_dashboard(dashboard_id: int, dashboard: CustomerDashboardCreate, db: Session = Depends(get_db)):
    db_dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.dashboard_id == dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found")
    for key, value in dashboard.dict().items():
        setattr(db_dashboard, key, value)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

@router.delete("/customer_dashboard/{dashboard_id}")
def delete_customer_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    db_dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.dashboard_id == dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found")
    db.delete(db_dashboard)
    db.commit()
    return {"detail": "Customer Dashboard deleted"}