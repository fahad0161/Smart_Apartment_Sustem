# Smart Apartment System

A comprehensive web-based apartment management system built for university database design course project.

## Project Overview

Smart Apartment System is a centralized platform that efficiently manages tenants, apartment units, financial transactions, and visitor records. It demonstrates understanding of relational database design, normalization, and CRUD operations.

## Features

### Core Features

1. **User Management**
   - Role-based access for Admins, Tenants, and Security Personnel
   - Secure authentication with password hashing
   - Profile management

2. **Apartment & Occupancy Tracking**
   - Real-time tracking of vacant and occupied units
   - Detailed apartment information (bedrooms, bathrooms, area, rent)

3. **Automated Billing System**
   - Generation and management of rent, electricity, water, and maintenance bills
   - Payment tracking and status updates
   - Due date management

4. **Visitor Management**
   - Digital logging of visitor entries and exits
   - Purpose of visit tracking
   - Real-time visitor count

5. **Service Requests**
   - System for tenants to submit maintenance requests
   - Priority-based request handling
   - Status tracking from submission to completion

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Backend | Python Flask |
| Database | MySQL |
| API | RESTful JSON API |

## Project Structure

```
smart-apartment-system/
├── database/
│   └── schema.sql          # MySQL database schema
├── backend/
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   ├── models.py           # Database models
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html      # Main dashboard
│   ├── apartments.html     # Apartment management
│   ├── users.html          # User management
│   ├── bills.html          # Billing management
│   ├── visitors.html       # Visitor management
│   ├── service-requests.html # Service requests
│   ├── css/
│   │   └── styles.css      # Custom styles
│   └── js/
│       ├── app.js          # Main application
│       ├── auth.js         # Authentication
│       ├── apartments.js   # Apartment logic
│       ├── bills.js        # Billing logic
│       ├── visitors.js      # Visitor logic
│       └── service_requests.js # Service request logic
├── SPEC.md                  # Project specification
└── README.md               # This file
```

## Installation & Setup

### Prerequisites

- Python 3.x
- MySQL 8.0
- Web browser

### Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE smart_apartment_db;
```

2. Run the schema file:
```bash
mysql -u root -p smart_apartment_db < database/schema.sql
```

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Update database configuration in `config.py`:
```python
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'smart_apartment_db'
```

4. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Open `frontend/index.html` in a web browser
2. Or serve the frontend using any HTTP server

## Demo Accounts

The system comes with pre-configured demo accounts:

| Username | Password | Role |
|----------|----------|------|
| admin | password123 | Admin |
| john_tenant | password123 | Tenant |
| security1 | password123 | Security |

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Users
- `GET /api/users` - Get all users
- `POST /api/users` - Create user
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

### Apartments
- `GET /api/apartments` - Get all apartments
- `POST /api/apartments` - Create apartment
- `PUT /api/apartments/:id` - Update apartment
- `DELETE /api/apartments/:id` - Delete apartment

### Bills
- `GET /api/bills` - Get all bills
- `POST /api/bills` - Create bill
- `PUT /api/bills/:id` - Update bill
- `POST /api/bills/:id/pay` - Pay bill

### Visitors
- `GET /api/visitors` - Get all visitors
- `POST /api/visitors` - Register visitor
- `PUT /api/visitors/:id/exit` - Log visitor exit

### Service Requests
- `GET /api/service-requests` - Get all requests
- `POST /api/service-requests` - Create request
- `PUT /api/service-requests/:id` - Update request

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

## Database Schema

### Users Table
- id, username, password, email, full_name, phone, role, apartment_id

### Apartments Table
- id, unit_number, floor, bedrooms, bathrooms, area_sqft, rent_amount, status, description

### Bills Table
- id, user_id, apartment_id, bill_type, amount, units_used, due_date, status, paid_date

### Visitors Table
- id, visitor_name, phone, apartment_id, purpose, entry_time, exit_time, checked_by, status

### Service Requests Table
- id, request_number, user_id, apartment_id, request_type, description, priority, status, assigned_to

## Course Learning Outcomes

This project demonstrates:
- Relational database design and normalization
- CRUD (Create, Read, Update, Delete) operations
- Role-based access control (RBAC)
- RESTful API design
- Full-stack web development
- Security best practices (password hashing, input validation)

## License

This project is for educational purposes.

## Authors

University Database Design Course Project Team
