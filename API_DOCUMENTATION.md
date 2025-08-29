# PilotsOntip Backend API Documentation

## Version 2.0.0
Last Updated: August 27, 2025

## Table of Contents
1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [AI Assistant / Chatbot](#ai-assistant--chatbot)
5. [Core APIs](#core-apis)
6. [Dashboard APIs](#dashboard-apis)
7. [Support APIs](#support-apis)
8. [Testing](#testing)
9. [Known Issues](#known-issues)

---

## Overview

PilotsOntip Backend is a comprehensive FastAPI-based REST API for a pilot booking/ride-hailing platform. The system connects customers with aviation services (pilots and aircraft operators) and includes an AI-powered chatbot for customer assistance.

### Base URL
```
http://localhost:8000
```

### API Documentation URLs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

### Technology Stack
- **Framework**: FastAPI 0.115.0
- **Database**: MySQL with SQLAlchemy ORM
- **Python**: 3.11+
- **Authentication**: PyJWT, passlib, bcrypt
- **Validation**: Pydantic 2.10.0

---

## Getting Started

### Installation
```bash
# Clone repository
git clone <repository-url>

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# Linux/Mac:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database tables
python databases/create_tables.py

# Run server
uvicorn main:app --reload
```

### Docker Setup
```bash
# Build image
docker build -t pilotsontip-backend .

# Run container
docker run -p 8000:8000 pilotsontip-backend

# Or use docker-compose
docker-compose up
```

---

## AI Assistant / Chatbot

The chatbot is a key feature that provides automated customer support with intelligent conversation management.

### Features
- **Automatic Case ID Generation**: Unique CASE IDs (e.g., CASE734507)
- **Name & Phone Extraction**: Automatically extracts user information from messages
- **Query Type Detection**: Identifies booking, support, pricing, and general queries
- **User Type Recognition**: Differentiates between new and existing users
- **Conversation Tracking**: Maintains complete conversation history

### Endpoints

#### Start/Continue Chat
```http
POST /chat/
```
**Request Body:**
```json
{
    "message": "Hi, I want to book a cab",
    "case_id": "CASE000001",  // Optional for continuing conversation
    "email": "user@example.com",  // Optional
    "phone": "9876543210"  // Optional
}
```

**Response:**
```json
{
    "case_id": "CASE734507",
    "response": "Welcome to PilotsOnTip! I'm your assistant. May I know your name?",
    "user_type": "new",
    "query_type": "booking",
    "conversation_status": "active",
    "suggestions": ["Book a ride", "Check prices", "Get support"]
}
```

#### Get Chat History
```http
GET /chat/{case_id}/history
```

#### Close Conversation
```http
PUT /chat/{case_id}/close
```

### Chatbot Flow Example
1. User: "Hi, I want to book a ride"
   - Bot: "Welcome! May I know your name?"
2. User: "My name is John"
   - Bot: "Thanks John! Please provide your phone number."
3. User: "My phone is 9876543210"
   - Bot: "Great John! Where would you like to be picked up from?"

---

## Core APIs

### Users

#### Create User
```http
POST /users/
```
**Request Body:**
```json
{
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "phone": "9876543210",
    "password": "securepassword",
    "user_type": "customer",
    "preferred_language": "English"
}
```

#### Get All Users
```http
GET /users/
```

#### Get User by ID
```http
GET /users/{user_id}
```

#### Update User
```http
PUT /users/{user_id}
```

#### Delete User
```http
DELETE /users/{user_id}
```

### Bookings

#### Create Booking
```http
POST /bookings/
```
**Request Body:**
```json
{
    "booking_id": "uuid-string",
    "booking_details": "Airport pickup",
    "vehicle_number": "MH12AB1234",
    "vehicle_type": "cab",
    "pickup_location": "Mumbai Airport",
    "drop_location": "Hotel",
    "booking_schedule": "2024-12-25T10:00:00",
    "number_of_person": 2,
    "booking_price": 500.00
}
```

#### Other Booking Endpoints
- `GET /bookings/` - List all bookings
- `GET /bookings/{booking_id}` - Get specific booking
- `PUT /bookings/{booking_id}` - Update booking
- `DELETE /bookings/{booking_id}` - Cancel booking

### Riders

#### Create Rider
```http
POST /rider/
```
**Request Body:**
```json
{
    "rider_name": "Mike Wilson",
    "rider_phone": "9876543210",
    "rider_email": "mike@example.com",
    "rider_license": "DL123456789",
    "rider_rating": 4.5,
    "vehicle_id": 1
}
```

#### Other Rider Endpoints
- `GET /rider/` - List all riders
- `GET /rider/{rider_id}` - Get rider details
- `PUT /rider/{rider_id}` - Update rider
- `DELETE /rider/{rider_id}` - Remove rider

### Vehicles

#### Create Vehicle
```http
POST /vehicles/
```
**Request Body:**
```json
{
    "vehicle_name": "Swift Dzire",
    "vehicle_number": "MH12AB1234",
    "vehicle_description": "White sedan, AC",
    "vehicle_rc": "RC123456",
    "vehicle_condition": "Excellent",
    "variant": "petrol",
    "vehicle_type": "cab",
    "vehicle_cab_type": "sedan"
}
```

### Partners

#### Create Partner
```http
POST /partners/
```
**Request Body:**
```json
{
    "number_of_users": 5,
    "partners_role": "Driver",
    "partner_type": "individual",
    "company_name": "Quick Cabs",
    "company_size": 10,
    "aadhare_card_number": "1234-5678-9012",
    "pan_card": "ABCDE1234F"
}
```

### Services

#### Create Service
```http
POST /services/
```
**Request Body:**
```json
{
    "service_name": "Airport Transfer",
    "service_description": "Premium airport service",
    "service_price": 1500.00,
    "service_duration": 60,
    "service_availability": true
}
```

### Payments

#### Create Payment
```http
POST /payments/
```
**Request Body:**
```json
{
    "booking_id": "booking-uuid",
    "mode_of_payment": "upi",  // Options: upi, cash, card, netbanking
    "payment_maker": "John Doe",
    "user_id": 1
}
```

**Response:**
```json
{
    "payment_id": 1,
    "booking_id": "booking-uuid",
    "reference_no": "auto-generated-uuid",  // System auto-generates unique transaction ID
    "mode_of_payment": "upi",
    "payment_maker": "John Doe",
    "user_id": 1
}
```

**Important Notes:**
- `reference_no` is automatically generated by the system - do NOT include in request
- Requires valid booking_id that exists in bookings table
- Each payment gets a unique reference number for transaction tracking

### Locations

#### Create Location
```http
POST /locations/
```
**Request Body:**
```json
{
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "pincode": "400001"
}
```

---

## Dashboard APIs

### Admin Dashboard

#### Create Admin Dashboard
```http
POST /admin_dashboard/
```
**Request Body:**
```json
{
    "total_users": 1000,
    "total_bookings": 500,
    "total_revenue": 50000.00,
    "active_riders": 25,
    "pending_approvals": 10
}
```

### Customer Dashboard

#### Create Customer Dashboard
```http
POST /customer_dashboard/
```
**Request Body:**
```json
{
    "customer_id": 1,
    "total_bookings": 10,
    "upcoming_bookings": 2,
    "completed_bookings": 8,
    "total_spent": 5000.00,
    "loyalty_points": 500
}
```

### Rider Dashboard

#### Create Rider Dashboard
```http
POST /rider_dashboard/
```
**Request Body:**
```json
{
    "rider_id": 1,
    "total_trips": 100,
    "completed_trips": 95,
    "cancelled_trips": 5,
    "total_earnings": 15000.00,
    "current_rating": 4.7,
    "active_status": true
}
```

---

## Support APIs

### Customer Support

#### Create Support Ticket
```http
POST /customer_support/
```
**Request Body:**
```json
{
    "full_name": "John Doe",
    "business_email": "john@company.com",
    "contact_number": "9876543210",
    "service_interest": "technical support",
    "message": "I need help with booking issues"
}
```

### Partner Queries

#### Create Partner Query
```http
POST /partner_query/
```
**Request Body:**
```json
{
    "partner_name": "ABC Transport",
    "partner_email": "abc@transport.com",
    "partner_phone": "9876543210",
    "query_type": "general",
    "query_message": "Need information about partnership"
}
```

### Feedback

#### Create Feedback
```http
POST /feedback/
```
**Request Body:**
```json
{
    "user_id": 1,
    "booking_id": "booking-uuid",
    "rating": 5,
    "feedback_text": "Excellent service",
    "feedback_type": "positive"
}
```

### Feedback Center

#### Create Feedback Center Entry
```http
POST /feedback_center/
```
**Request Body:**
```json
{
    "feedback_type": "rider",
    "user_id": 1,
    "rating": 4,
    "feedback_text": "Good service overall",
    "created_by": 1
}
```

---

## Testing

### Using Postman Collection
1. Import `PilotsOntip_API_Collection_Complete.json` into Postman
2. Set up environment variables for IDs (booking_id, user_id, etc.)
3. Run requests in sequence for proper flow

### Automated Testing
```bash
# Run the chatbot test script
python test_assistant.py
```

### Test Coverage
- ✅ AI Chatbot with conversation flow
- ✅ User registration and management
- ✅ Booking creation and tracking
- ✅ Payment processing (with valid booking_id)
- ✅ Dashboard metrics
- ✅ Support ticket management
- ✅ Feedback system

---

## Known Issues

### Current Limitations
1. **Payment API**: Requires valid booking_id due to foreign key constraint
2. **Authentication**: JWT authentication not yet implemented
3. **Rate Limiting**: No rate limiting implemented
4. **File Uploads**: Profile photos and documents upload not implemented

### Common Errors

#### Foreign Key Constraint Error
```json
{
    "detail": "Cannot add or update a child row: a foreign key constraint fails"
}
```
**Solution**: Ensure referenced ID exists in parent table.

#### Validation Error (422)
```json
{
    "detail": [
        {
            "loc": ["body", "field_name"],
            "msg": "Field required",
            "type": "missing"
        }
    ]
}
```
**Solution**: Check request body for required fields.

---

## Database Schema

### Key Tables
- **users**: Customer and partner accounts
- **user_profile**: AI chatbot conversation profiles
- **bookings**: Ride/flight reservations
- **payments**: Transaction records
- **vehicles**: Fleet management
- **partners**: Service providers
- **riders**: Driver/pilot information
- **locations**: Geographic data
- **services**: Available services
- **dashboards**: Analytics data
- **feedback**: Customer reviews
- **customer_support**: Support tickets

### Relationships
- Users → Bookings (One to Many)
- Bookings → Payments (One to Many)
- Riders → Vehicles (Many to One)
- Users → Feedback (One to Many)

---

## Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

## Contact & Support

For API issues or questions:
- Check Swagger documentation at `/docs`
- Review error messages for specific field requirements
- Ensure database is properly configured
- Verify all dependencies are installed

## Version History

### v2.0.0 (Current)
- Added AI Chatbot with intelligent conversation management
- Implemented name and phone extraction
- Added 90+ API endpoints
- Complete CRUD operations for all entities
- Dashboard management system
- Comprehensive feedback system

### v1.0.0
- Initial release
- Basic CRUD operations
- User management
- Booking system