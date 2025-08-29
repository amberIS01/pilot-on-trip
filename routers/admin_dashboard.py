-from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.admin_dashboard_model import AdminDashboard
from schemes.admin_dashboard import AdminDashboardCreate, AdminDashboardResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admin_dashboard/", response_model=AdminDashboardResponse)
def create_admin_dashboard(dashboard: AdminDashboardCreate, db: Session = Depends(get_db)):
    new_dashboard = AdminDashboard(**dashboard.dict())
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    return new_dashboard

@router.get("/admin_dashboard/", response_model=List[AdminDashboardResponse])
def list_admin_dashboards(db: Session = Depends(get_db)):
    return db.query(AdminDashboard).all()

@router.get("/admin_dashboard/{admin_dashboard_id}", response_model=AdminDashboardResponse)
def get_admin_dashboard(admin_dashboard_id: int, db: Session = Depends(get_db)):
    dashboard = db.query(AdminDashboard).filter(AdminDashboard.admin_dashboard_id == admin_dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Admin Dashboard not found")
    return dashboard

@router.put("/admin_dashboard/{admin_dashboard_id}", response_model=AdminDashboardResponse)
def update_admin_dashboard(admin_dashboard_id: int, dashboard: AdminDashboardCreate, db: Session = Depends(get_db)):
    db_dashboard = db.query(AdminDashboard).filter(AdminDashboard.admin_dashboard_id == admin_dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Admin Dashboard not found")
    for key, value in dashboard.dict().items():
        setattr(db_dashboard, key, value)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

@router.delete("/admin_dashboard/{admin_dashboard_id}")
def delete_admin_dashboard(admin_dashboard_id: int, db: Session = Depends(get_db)):
    db_dashboard = db.query(AdminDashboard).filter(AdminDashboard.admin_dashboard_id == admin_dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Admin Dashboard not found")
    db.delete(db_dashboard)
    db.commit()
    return {"detail": "Admin Dashboard deleted"}
