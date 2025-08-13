# PilotsOntip-Backend

## Project Overview
PilotsOntip-Backend is a comprehensive FastAPI-based backend service for a pilot booking/ride-hailing platform. It connects customers who need flights with pilots and aircraft operators, similar to ride-sharing services but specialized for aviation services.

### Core Features
- **User Management**: Customers and partners with role-based access
- **Booking System**: Flight/ride reservations with UUID tracking
- **Partner Management**: Pilot/operator onboarding and verification
- **Vehicle Management**: Aircraft and transportation fleet management
- **Payment Processing**: Secure transaction handling
- **Feedback System**: Ratings and reviews for service quality
- **Dashboard Systems**: Admin, customer, and rider interfaces
- **Customer Support**: Query management and support ticketing
- **Location Services**: Geographic data for pickups and destinations

## Technology Stack
- **Backend**: Python 3.11+ with FastAPI 0.115.0
- **Database**: MySQL with SQLAlchemy 1.4.53 ORM
- **Authentication**: PyJWT 2.10.1, passlib 1.7.4, bcrypt 4.2.1
- **Validation**: Pydantic 2.10.0 for request/response schemas
- **Email**: fastapi-mail 1.4.1 with aiosmtplib 2.0.2
- **Server**: uvicorn 0.31.1
- **Testing**: pytest 8.3.4
- **Containerization**: Docker with docker-compose
- **Database Driver**: PyMySQL 1.1.1

## Architecture & Folder Structure

### Database Design
The system uses a comprehensive relational database with the following core entities:
- **Users**: Customers and partners with different roles
- **Partners**: Service providers (pilots/operators) with verification
- **Vehicles**: Aircraft/transportation fleet with specifications
- **Bookings**: Ride/flight reservations with UUID tracking
- **Payments**: Transaction records with reference numbers
- **Locations**: Geographic data for service areas
- **Feedback Systems**: Reviews and support ticketing
- **Dashboard Data**: Analytics for admin, customer, and rider views

### Project Structure
- **main.py**: FastAPI application entry point with router imports
- **models/**: SQLAlchemy ORM models for all database entities
  - User, Partner, Vehicle, Booking, Payment models
  - Dashboard models (admin, customer, rider)
  - Feedback and support models
- **routers/**: FastAPI endpoint definitions organized by resource
  - RESTful API routes for CRUD operations
  - Consistent dependency injection pattern
- **schemes/**: Pydantic schemas for request/response validation
- **databases/**: Database connection and configuration
  - `database.py`: MySQL connection with SQLAlchemy
  - `create_tables.py`: Database initialization
- **requirements.txt**: Python dependencies with versions
- **Dockerfile & docker-compose.yaml**: Containerization setup

## Setup Instructions

1. **Clone the repository**
2. **Create and activate a Python virtual environment**
   - Windows: `python -m venv env` then `env\Scripts\activate`
3. **Install dependencies**
   - `pip install -r requirements.txt`
4. **Configure MySQL database**
   - Ensure MySQL is running locally and update connection details in `databases/database.py` if needed.
5. **Run the application**
   - `uvicorn main:app --reload`
6. **(Optional) Run with Docker**
   - Build: `docker build -t pilotsontip-backend .`
   - Run: `docker run -p 8000:8000 pilotsontip-backend`

## Best Practices
- Use connection pooling and proper error handling for MySQL connections.
- Follow least privilege principle for database users.
- Regularly backup your database.
- Validate all API inputs using Pydantic schemas.
- Keep dependencies updated and use virtual environments.

## API Endpoints Overview
The application provides RESTful APIs for:
- **User Management**: Registration, authentication, profile management
- **Booking Operations**: Create, read, update booking requests
- **Partner Services**: Partner registration, verification, management
- **Vehicle Management**: Fleet registration and specifications
- **Payment Processing**: Transaction handling and records
- **Feedback System**: Reviews, ratings, and support tickets
- **Dashboard Data**: Analytics and reporting for different user roles

## Development Status
- ✅ **Core Models**: All database models implemented
- ✅ **Basic CRUD**: Essential API endpoints functional
- ✅ **Database Setup**: MySQL integration with SQLAlchemy
- ✅ **Containerization**: Docker setup ready
- 🔄 **In Progress**: Authentication, validation, error handling
- 📋 **Planned**: AI assistant integration, comprehensive testing

## Production Considerations
- **Security**: Implement JWT authentication and authorization
- **Configuration**: Move database credentials to environment variables
- **Error Handling**: Add comprehensive error management
- **Testing**: Implement unit and integration tests
- **Monitoring**: Add logging and performance monitoring
- **Documentation**: Generate API documentation with OpenAPI/Swagger

## Notes
- Backend runs on port 8000 by default
- MySQL database required (local or containerized)
- Database schema designed with dbdiagram.io for consistency
- Future AI assistant integration planned for customer support enhancement