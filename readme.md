# PilotsOntip Backend API

## 🚀 Overview

PilotsOntip Backend is a comprehensive FastAPI-based REST API platform designed for aviation service booking and ride-hailing operations. The system features an AI-powered chatbot, complete CRUD operations for all business entities, real-time booking and payment processing, and multi-dashboard analytics.

### Key Features

- 🤖 **AI Chatbot System** - Intelligent conversation management with case ID generation
- ✈️ **Aviation Booking Platform** - Connect customers with pilots and aircraft operators
- 💳 **Payment Processing** - Multiple payment modes with auto-generated transaction references
- 📊 **Multi-Dashboard System** - Separate dashboards for Admin, Customer, and Rider
- 🔒 **Security Ready** - JWT authentication framework (ready for implementation)
- 🐳 **Docker Support** - Full containerization with Docker Compose
- 📝 **Complete API Documentation** - Swagger UI and ReDoc integration

## 🛠️ Technology Stack

| Component        | Technology                         |
| ---------------- | ---------------------------------- |
| Framework        | FastAPI 0.115.0                    |
| Language         | Python 3.11+                       |
| Database         | MySQL with SQLAlchemy ORM          |
| Validation       | Pydantic 2.10.0                    |
| Authentication   | PyJWT                              |
| Containerization | Docker & Docker Compose            |
| API Testing      | Postman Collection (90+ endpoints) |

## 📋 Prerequisites

- Python 3.11 or higher
- MySQL 8.0 or higher
- Docker & Docker Compose (optional)
- Git

## 🚀 Quick Start

### Local Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/pilotsontip/backend.git
cd pilotsontip-backend
```

2. **Create virtual environment**

```bash
python -m venv env
# On Windows
env\Scripts\activate
# On Linux/Mac
source env/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure database**

- Update MySQL connection string in `databases/database.py`
- Default: `mysql+pymysql://root:sahil@localhost:3306/pilotsontip`

5. **Create database tables**

```bash
python databases/create_tables.py
```

6. **Start the server**

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Setup (Recommended)

```bash
# Start both MySQL and Backend
docker-compose up

# Start with rebuild
docker-compose up --build
```

2. **Using Docker (Backend Only)**

```bash
# Build image
docker build -t pilotsontip-backend .

# Run container
docker run -p 8000:8000 pilotsontip-backend
```

## 📁 Project Structure

```
pilotsontip-backend/
├── databases/          # Database configuration and table creation
│   ├── database.py    # SQLAlchemy engine and session
│   └── create_tables.py # Table creation script
├── models/            # SQLAlchemy ORM models (17 tables)
│   ├── user_model.py
│   ├── booking_model.py
│   ├── payment_model.py
│   ├── customer_dashboard_model.py # Updated with booking_id
│   └── ...
├── routers/           # FastAPI route handlers
│   ├── chatbot.py     # AI chatbot endpoints
│   ├── user.py
│   ├── booking.py
│   ├── customer_dashboard.py # Enhanced with new endpoints
│   └── ...
├── schemes/           # Pydantic validation schemas
│   ├── user.py
│   ├── booking.py
│   └── ...
├── main.py           # FastAPI application entry point
├── requirements.txt  # Python dependencies
├── Dockerfile       # Multi-stage Docker build
└── docker-compose.yaml # Full stack orchestration
```

## 🗄️ Database Schema

The system uses **17 interconnected tables**:

### Core Tables

- `users` - Customer and partner accounts
- `bookings` - Ride/flight reservations
- `payments` - Transaction records (auto-generated reference_no)
- `vehicles` - Fleet management
- `riders` - Driver/pilot profiles
- `partners` - Service providers

### Dashboard Tables (v3.0 Updates)

- `customer_dashboards` - Customer metrics
  - NEW: `booking_id` field for booking association
  - REMOVED: `preferences` field
- `admin_dashboard` - Administrative analytics
- `rider_dashboard` - Driver/pilot performance

### Support Tables

- `user_profile` - AI chatbot conversation profiles
- `customer_support` - Support ticket system
- `feedback` - Customer reviews and ratings
- `locations` - Geographic data
- `services` - Available service offerings

## 🤖 AI Chatbot Features

The intelligent chatbot system provides:

- **Automatic Case ID Generation** (e.g., CASE734507)
- **Smart Information Extraction** - Names and phone numbers from messages
- **Query Type Detection** - Booking, support, pricing, general
- **User Type Recognition** - New vs existing customers
- **Conversation History** - Complete tracking with status

### Chatbot API Usage

```python
# Start conversation
POST /chat/
{
    "message": "Hi, I want to book a ride"
}

# Continue with case ID
POST /chat/
{
    "message": "My name is John",
    "case_id": "CASE734507"
}

# Get conversation history
GET /chat/CASE734507/history
```

## 💳 Payment System

### Important Notes

- `reference_no` is **automatically generated** by the system
- Do NOT include `reference_no` in payment creation requests
- Each payment gets a unique UUID for transaction tracking

### Payment API Example

```json
// Request (NO reference_no needed)
POST /payments/
{
    "booking_id": "existing-booking-uuid",
    "mode_of_payment": "upi",
    "payment_maker": "John Doe",
    "user_id": 1
}

// Response (includes auto-generated reference_no)
{
    "payment_id": 1,
    "booking_id": "existing-booking-uuid",
    "reference_no": "550e8400-e29b-41d4-a716",  // AUTO-GENERATED
    "mode_of_payment": "upi",
    "payment_maker": "John Doe",
    "user_id": 1
}
```

## 📡 API Endpoints

### Quick Overview

- **Base URL**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/`

### Main Routers (90+ endpoints)

| Router             | Base Path                | Description                     |
| ------------------ | ------------------------ | ------------------------------- |
| AI Chatbot         | `/chat/`               | Intelligent conversation system |
| Users              | `/users/`              | User management                 |
| Bookings           | `/bookings/`           | Reservation system              |
| Payments           | `/payments/`           | Transaction processing          |
| Customer Dashboard | `/customer_dashboard/` | Customer analytics              |
| Vehicles           | `/vehicles/`           | Fleet management                |
| Riders             | `/rider/`              | Driver profiles                 |

### Customer Dashboard Updates (v3.0)

New endpoints for enhanced dashboard functionality:

- `GET /customer_dashboard/user/{user_id}` - Get dashboard by user
- `GET /customer_dashboard/booking/{booking_id}` - Get dashboards by booking
- `PATCH /customer_dashboard/{id}/activity` - Update activity only

## 🔐 Environment Variables

Create a `.env` file for configuration:

```env
# Database
MYSQL_ROOT_PASSWORD=sahil
MYSQL_DATABASE=pilotsontip
MYSQL_USER=pilotsontip
MYSQL_PASSWORD=pilotsontip123

# Application
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# AI Chatbot
CHATBOT_ENABLED=true
CHATBOT_MODEL=gpt-3.5-turbo
CHATBOT_API_KEY=your-api-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🧪 Testing

### Using Postman Collection

1. Import `PilotsOntip_API_Collection.json` into Postman
2. Set environment variables in Postman
3. Run the collection to test all 90+ endpoints

### Manual Testing

```bash
# Health check
curl http://localhost:8000/

# Create a booking
curl -X POST http://localhost:8000/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"booking_id": "uuid-here", "booking_details": "Airport pickup"}'

# Create a payment (no reference_no needed)
curl -X POST http://localhost:8000/payments/ \
  -H "Content-Type: application/json" \
  -d '{"booking_id": "uuid", "mode_of_payment": "upi", "payment_maker": "John", "user_id": 1}'
```

### Automated Testing

```bash
# Run test suite
python test_assistant.py
```

## 🐳 Docker Commands

### Development

```bash
# Start all services
docker-compose up

# Start with rebuild
docker-compose up --build

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Clean up volumes
docker-compose down -v
```

### Production

```bash
# Build with metadata
docker build \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VERSION=3.0.0 \
  -t pilotsontip-backend:latest .

# Run with environment file
docker run --env-file .env -p 8000:8000 pilotsontip-backend:latest
```

## 📊 Database Management

### Create/Update Tables

```bash
python databases/create_tables.py
```

### Access Database

Connect to MySQL directly:
- Host: `localhost`
- Port: `3306`
- Username: `root`
- Password: `sahil`
- Database: `pilotsontip`

### Database Migration (for existing systems)

To add the new `booking_id` field to `customer_dashboards`:

```sql
ALTER TABLE customer_dashboards 
ADD COLUMN booking_id VARCHAR(36),
ADD FOREIGN KEY (booking_id) REFERENCES bookings(booking_id);
```

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**

   - Verify MySQL is running: `sudo service mysql status`
   - Check connection string in `databases/database.py`
   - Ensure database `pilotsontip` exists: `CREATE DATABASE pilotsontip;`
2. **Payment API Foreign Key Error**

   - Ensure booking_id exists in bookings table
   - Reference_no is auto-generated, don't include in request
   - Check user_id exists in users table
3. **Docker Build Fails**

   - Check Docker daemon: `docker info`
   - Verify port 8000 is free: `lsof -i :8000`
   - Clear Docker cache: `docker system prune -a`
4. **Import Errors**

   - Activate virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Check Python version: `python --version` (should be 3.11+)
5. **Customer Dashboard Issues**

   - Ensure user_id exists before creating dashboard
   - booking_id is optional but must exist if provided
   - Use proper UUID format for booking_id

## 📚 Documentation

- **API Documentation**: Available at `/docs` when server is running
- **Postman Collection**: `PilotsOntip_API_Collection.json` (updated v3.0)
- **Word Documentation**: `PilotsOntip Backend Project Documentation v3.0.docx`
- **Development Guide**: `CLAUDE.md`
- **API Examples**: `API_DOCUMENTATION.md`

## 🚀 Version History

### v3.0.0 (Current - December 2024)

- ✅ Added `booking_id` field to customer_dashboard
- ✅ Removed `preferences` field from customer_dashboard
- ✅ Enhanced customer dashboard router with new endpoints
- ✅ Fixed payment API (clarified reference_no auto-generation)
- ✅ Enhanced Docker configuration with multi-stage build
- ✅ Simplified docker-compose for essential services
- ✅ Updated Postman collection with all changes
- ✅ Comprehensive documentation update

### v2.0.0

- AI Chatbot integration with case management
- Complete CRUD operations for all entities
- Docker support with basic configuration
- Initial Postman collection

### v1.0.0

- Initial release
- Basic booking system
- User management

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Write clear commit messages
- Update documentation for new features
- Add tests for new endpoints
- Ensure all tests pass before PR

## 📄 License

This project is proprietary software. All rights reserved.

## 📞 Support

For technical support or questions:

- Check API documentation at `/docs`
- Review error messages for field requirements
- Ensure all dependencies are installed
- Verify database configuration
- Check logs in `/app/logs` directory

## 🏗️ Roadmap

### Near Term (Q1 2025)

- [ ] Complete JWT authentication implementation
- [ ] Add rate limiting
- [ ] Implement WebSocket for real-time updates
- [ ] Add file upload for documents/photos

### Medium Term (Q2 2025)

- [ ] Machine learning for demand prediction
- [ ] Payment gateway integration
- [ ] Multi-language support
- [ ] Mobile app API extensions

### Long Term (2025+)

- [ ] Microservices architecture
- [ ] Kubernetes deployment
- [ ] GraphQL API option
- [ ] Advanced analytics dashboard

---

**Built with ❤️ by PilotsOntip Team**

*Last Updated: December 2024*
