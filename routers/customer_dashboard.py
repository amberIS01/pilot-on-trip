from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.customer_dashboard_model import CustomerDashboard
from schemes.customer_dashboard import CustomerDashboardCreate, CustomerDashboardUpdate, CustomerDashboardResponse
from typing import List, Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/customer_dashboard/", response_model=CustomerDashboardResponse)
def create_customer_dashboard(dashboard: CustomerDashboardCreate, db: Session = Depends(get_db)):
    """
    Create a new customer dashboard entry.
    
    Args:
        dashboard: CustomerDashboardCreate schema with user_id, last_login, activity_summary, booking_id
        db: Database session
        
    Returns:
        CustomerDashboardResponse: Created dashboard with generated dashboard_id
        
    Raises:
        HTTPException: If user_id or booking_id doesn't exist
    """
    # Check if dashboard already exists for user
    existing = db.query(CustomerDashboard).filter(CustomerDashboard.user_id == dashboard.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Dashboard already exists for this user")
    
    new_dashboard = CustomerDashboard(**dashboard.dict())
    db.add(new_dashboard)
    db.commit()
    db.refresh(new_dashboard)
    return new_dashboard

@router.get("/customer_dashboard/", response_model=List[CustomerDashboardResponse])
def list_customer_dashboards(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all customer dashboards with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List[CustomerDashboardResponse]: List of customer dashboards
    """
    dashboards = db.query(CustomerDashboard).offset(skip).limit(limit).all()
    return dashboards

@router.get("/customer_dashboard/{dashboard_id}", response_model=CustomerDashboardResponse)
def get_customer_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """
    Get a specific customer dashboard by ID.
    
    Args:
        dashboard_id: The dashboard ID to retrieve
        db: Database session
        
    Returns:
        CustomerDashboardResponse: The requested dashboard
        
    Raises:
        HTTPException: If dashboard not found
    """
    dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.dashboard_id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found")
    return dashboard

@router.get("/customer_dashboard/user/{user_id}", response_model=CustomerDashboardResponse)
def get_customer_dashboard_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get customer dashboard by user ID.
    
    Args:
        user_id: The user ID to find dashboard for
        db: Database session
        
    Returns:
        CustomerDashboardResponse: The user's dashboard
        
    Raises:
        HTTPException: If dashboard not found for user
    """
    dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.user_id == user_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found for this user")
    return dashboard

@router.get("/customer_dashboard/booking/{booking_id}", response_model=List[CustomerDashboardResponse])
def get_customer_dashboards_by_booking(booking_id: str, db: Session = Depends(get_db)):
    """
    Get all customer dashboards associated with a booking ID.
    
    Args:
        booking_id: The booking UUID to search for
        db: Database session
        
    Returns:
        List[CustomerDashboardResponse]: List of dashboards with this booking_id
    """
    dashboards = db.query(CustomerDashboard).filter(CustomerDashboard.booking_id == booking_id).all()
    if not dashboards:
        raise HTTPException(status_code=404, detail="No dashboards found for this booking")
    return dashboards

@router.put("/customer_dashboard/{dashboard_id}", response_model=CustomerDashboardResponse)
def update_customer_dashboard(
    dashboard_id: int, 
    dashboard: CustomerDashboardUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing customer dashboard.
    
    Args:
        dashboard_id: The dashboard ID to update
        dashboard: CustomerDashboardUpdate schema with fields to update
        db: Database session
        
    Returns:
        CustomerDashboardResponse: Updated dashboard
        
    Raises:
        HTTPException: If dashboard not found
    """
    db_dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.dashboard_id == dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found")
    
    # Only update provided fields
    update_data = dashboard.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_dashboard, key, value)
    
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

@router.patch("/customer_dashboard/{dashboard_id}/activity", response_model=CustomerDashboardResponse)
def update_dashboard_activity(
    dashboard_id: int,
    activity_summary: str,
    db: Session = Depends(get_db)
):
    """
    Update only the activity summary of a dashboard.
    
    Args:
        dashboard_id: The dashboard ID to update
        activity_summary: New activity summary text
        db: Database session
        
    Returns:
        CustomerDashboardResponse: Updated dashboard
        
    Raises:
        HTTPException: If dashboard not found
    """
    db_dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.dashboard_id == dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found")
    
    db_dashboard.activity_summary = activity_summary
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

@router.delete("/customer_dashboard/{dashboard_id}")
def delete_customer_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer dashboard.
    
    Args:
        dashboard_id: The dashboard ID to delete
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If dashboard not found
    """
    db_dashboard = db.query(CustomerDashboard).filter(CustomerDashboard.dashboard_id == dashboard_id).first()
    if not db_dashboard:
        raise HTTPException(status_code=404, detail="Customer Dashboard not found")
    
    db.delete(db_dashboard)
    db.commit()
    return {"detail": "Customer Dashboard deleted successfully"}