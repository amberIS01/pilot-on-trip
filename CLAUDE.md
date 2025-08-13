# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- Local development: `uvicorn main:app --reload`
- Production: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Docker build: `docker build -t pilotsontip-backend .`
- Docker run: `docker run -p 8000:8000 pilotsontip-backend`
- Docker Compose: `docker-compose up`

### Testing
- Run tests: `pytest` (when test files are added)
- The project includes pytest dependency but tests need to be implemented

### Database
- Database connection: MySQL via SQLAlchemy with PyMySQL driver
- Connection string format: `mysql+pymysql://root:sahil@localhost:3306/pilotsontip`
- Tables are created via `databases/create_tables.py`
- Engine configured with `echo=True` for SQL logging

## Architecture Overview

### Core Structure
This is a FastAPI-based backend for a pilot booking platform with a modular architecture:

- **main.py**: FastAPI app entry point that includes all routers
- **models/**: SQLAlchemy ORM models (User, Partner, Vehicle, Booking, Payment, etc.)
- **routers/**: FastAPI route handlers organized by resource
- **schemes/**: Pydantic schemas for request/response validation
- **databases/**: Database connection and table creation logic

### Database Design
The system uses MySQL with SQLAlchemy ORM. Key entities include:
- Users (customers and partners)
- Partners (service providers)
- Vehicles
- Bookings
- Payments
- Locations
- Services
- Dashboard entities (admin, customer, rider)
- Feedback system

### Router Pattern
Each router follows a consistent pattern:
```python
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/resource/")
def create_resource(item: Schema, db: Session = Depends(get_db)):
    # CRUD operations
```

### Model Conventions
- All models inherit from `databases.database.Base`
- Primary keys follow pattern: `{table_name}_id` (e.g., `user_id`, `partner_id`)
- Foreign keys reference related tables
- Enums are defined as `str, enum.Enum` classes
- DateTime fields for tracking creation/updates

## Technology Stack
- **Framework**: FastAPI 0.115.0
- **Database**: MySQL with SQLAlchemy 1.4.53 and PyMySQL 1.1.1
- **Validation**: Pydantic 2.10.0
- **Authentication**: PyJWT 2.10.1, passlib 1.7.4, bcrypt 4.2.1
- **Email**: fastapi-mail 1.4.1, aiosmtplib 2.0.2
- **Testing**: pytest 8.3.4
- **Server**: uvicorn 0.31.1

## Database Connection
The database connection is hardcoded in `databases/database.py`. For production deployments, consider using environment variables for database credentials instead of the current hardcoded connection string.

## Key Development Notes
- Router modules are imported and included in main.py
- Database sessions are managed via dependency injection using `get_db()`
- Models use SQLAlchemy declarative base
- The application runs on port 8000 by default
- No environment variable configuration is currently implemented
- Table creation is handled separately via `create_tables.py`