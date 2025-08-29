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

### Database Operations
- Create all tables: `python databases/create_tables.py`
- Database connection: MySQL via SQLAlchemy with PyMySQL driver
- Connection string: `mysql+pymysql://root:sahil@localhost:3306/pilotsontip`
- Engine configured with `echo=True` for SQL logging in development

### API Documentation
- Access Swagger UI: `http://localhost:8000/docs`
- Access ReDoc: `http://localhost:8000/redoc`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Architecture Overview

### Project Purpose
PilotsOntip is a pilot booking/ride-hailing platform connecting customers with aviation services (pilots and aircraft operators), similar to ride-sharing but for aviation.

### Core Structure
This is a FastAPI-based backend with modular architecture:

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
Each router follows a consistent CRUD pattern with dependency injection:
```python
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/resource/")
def create_resource(item: SchemaCreate, db: Session = Depends(get_db)):
    # Check for duplicates if applicable
    # Create new instance: Model(**item.dict())
    # Add, commit, refresh, return

@router.get("/resource/", response_model=List[SchemaResponse])
def list_resources(db: Session = Depends(get_db)):
    return db.query(Model).all()
```

### Model Conventions
- All models inherit from `databases.database.Base`
- Primary keys follow pattern: `{table_name}_id` (e.g., `user_id`, `partner_id`)
- Foreign keys reference related tables
- Enums are defined as `str, enum.Enum` classes
- DateTime fields for tracking creation/updates

## New Routers and Models
When adding new features, recent additions include:
- **user_profile**: User profile management
- **chatbot**: AI assistant integration (in progress)

New routers should be imported and included in main.py following existing patterns.

## API Endpoints Pattern
- All endpoints follow RESTful conventions
- Standard CRUD operations: POST (create), GET (list/read), PUT (update), DELETE (delete)
- Primary key pattern: `/{resource}/{resource_id}` (e.g., `/users/{user_id}`)
- Response models defined in schemes for type safety

## Database Connection
The database connection is hardcoded in `databases/database.py`. For production deployments, consider using environment variables for database credentials instead of the current hardcoded connection string.

## Key Development Notes  
- Router modules are imported and included in main.py
- Database sessions are managed via dependency injection using `get_db()`
- Models use SQLAlchemy declarative base
- The application runs on port 8000 by default
- No environment variable configuration is currently implemented
- Table creation is handled separately via `create_tables.py`
- SQL queries are logged to console when `echo=True` in engine configuration

## Testing Approach
While pytest is configured, no tests are currently implemented. When adding tests:
- Create test files in a `tests/` directory
- Use pytest fixtures for database sessions
- Mock external dependencies
- Run with `pytest` command