# Smart_Apartment_Sustem
Md. Abu Houraira Fahad (2023200000090)
Shahriar Sabbir (2023200000210)
Rahad Hossen (2023200000332)
Md Parvez Hossen (2023200000266)
Sumaya Akter Shumi (2023200000262)


# Smart Apartment Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)
![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-purple?style=for-the-badge&logo=bootstrap)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)

### A Modern Digital Solution for Apartment Administration & Tenant Management

</div>

---

# Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Future Enhancements](#future-enhancements)
- [Testing Strategy](#testing-strategy)
- [Team Contributions](#team-contributions)
- [Academic Context](#academic-context)
- [License](#license)

---

# Project Overview

The **Smart Apartment Management System** is a web-based apartment administration platform designed to streamline and digitize apartment-related operations, including tenant management, apartment allocation, billing, maintenance services, and administrative monitoring.

Traditional apartment management often relies on manual record-keeping, which can lead to inefficiency, delayed communication, billing errors, and poor maintenance coordination. This system addresses these issues through an integrated digital platform that enables both **administrators** and **tenants** to manage apartment-related activities efficiently.

The application is developed using **Python Flask** for backend services, **MySQL** for database management, and **HTML, CSS, Bootstrap, and JavaScript** for the user interface.

---

# Problem Statement

Managing apartment operations manually creates several challenges:

- Difficulty in maintaining tenant records
- Delayed bill generation and tracking
- Poor communication between tenants and management
- Lack of maintenance request tracking
- Time-consuming administrative operations

The Smart Apartment Management System aims to solve these issues through automation and centralized management.

---

# Objectives

The major objectives of this project are:

- Digitize apartment administration processes
- Provide secure authentication and authorization
- Manage apartment tenants effectively
- Simplify bill generation and monitoring
- Improve maintenance request handling
- Enhance communication between tenants and management
- Reduce manual workload and operational inefficiencies

---

# Core Features

## 1. Authentication & Authorization

The system includes a secure login and access control mechanism.

### Features
- User Registration
- Login Authentication
- Role-Based Authorization
- Session/Token-Based Authentication
- Protected API Routes

### Supported Roles

| Role | Access Level |
|------|--------------|
| **Admin** | Full system access |
| **Tenant** | Limited apartment-specific access |

---

## 2. User Management

Administrators can manage tenant accounts through a centralized dashboard.

### Functionalities
- Create New Users
- Update User Information
- Delete Users
- Search and View Tenant Information
- User Role Management

---

## 3. Apartment Management

The system maintains apartment-related information efficiently.

### Functionalities
- Apartment Allocation
- Apartment Information Tracking
- Apartment Status Management
- Tenant–Apartment Association

---

## 4. Bill Management

Digital billing features improve transparency and reduce manual accounting effort.

### Functionalities
- Bill Generation
- Utility Bill Tracking
- Monthly Payment Monitoring
- Tenant Bill History

---

## 5. Service Request Management

Tenants can request maintenance services digitally.

### Available Service Categories
- Plumbing
- Electrical
- Painting
- Cleaning
- Appliance Repair
- Other Maintenance Services

### Features
- Request Submission
- Priority Management
- Request Status Tracking
- Maintenance Monitoring

---

## 6. Dashboard & Analytics

The dashboard provides system insights and operational visibility.

### Dashboard Features
- User Overview
- Apartment Statistics
- Bill Monitoring
- Service Request Overview

---

# System Architecture

The project follows a **client-server architecture**:

```text
Frontend (HTML/CSS/Bootstrap)
            │
            ▼
      Flask REST API
            │
            ▼
        MySQL Database
```

### Architecture Components

#### Frontend Layer
Responsible for:
- User Interface
- User Interaction
- Data Presentation

#### Backend Layer
Responsible for:
- Business Logic
- Authentication
- API Handling
- Database Communication

#### Database Layer
Responsible for:
- Data Storage
- Query Processing
- Relationship Management

---

# Technology Stack

## Backend Technologies

| Technology | Purpose |
|------------|---------|
| Python | Core Programming Language |
| Flask | Backend Framework |
| Flask-CORS | Cross-Origin Requests |
| bcrypt | Password Security |
| PyMySQL | Database Connectivity |

---

## Frontend Technologies

| Technology | Purpose |
|------------|---------|
| HTML5 | Page Structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Client-Side Functionality |

---

## Database

| Technology | Purpose |
|------------|---------|
| MySQL | Relational Database Management |

---

# Project Structure

```plaintext
Smart_Apartment_Sustem/
│
├── Backend/
│   ├── app.py
│   ├── config.py
│   └── users.py
│
├── Frontend/
│   └── users.html
│
├── dashboard.html
├── apartment.html
├── Billtable.html
├── models.py
├── requirements.txt
├── README.md
└── env.txt
```

---

# Installation & Setup

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/Smart_Apartment_Sustem.git
```

Navigate to the project directory:

```bash
cd Smart_Apartment_Sustem
```

---

## Step 2: Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

# Database Configuration

Create a database in MySQL:

```sql
CREATE DATABASE smart_apartment;
```

Update your database credentials inside `config.py`:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "smart_apartment"
DB_PORT = 3306
```

---

# Running the Application

Run the Flask server:

```bash
python app.py
```

Application URL:

```text
http://localhost:5000
```

---

# API Documentation

## Authentication APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate user |

---

## User Management APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Retrieve all users |
| POST | `/api/users` | Add a user |
| GET | `/api/users/<id>` | Retrieve single user |
| PUT | `/api/users/<id>` | Update user |
| DELETE | `/api/users/<id>` | Delete user |

---

## Bill Management APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bills` | Retrieve bills |
| POST | `/api/bills` | Create bills |

---

# Security Features

The application implements several security measures:

- Role-Based Access Control (RBAC)
- Token Authentication
- Password Encryption using bcrypt
- Protected API Endpoints
- Session Management
- Error Handling

---

# Future Enhancements

Planned future improvements include:

- Online Payment Gateway
- Mobile Application Integration
- Push Notifications
- Email/SMS Alerts
- AI-Based Smart Monitoring
- Real-Time Maintenance Tracking
- Tenant Chat Support

---

# Testing Strategy

The system APIs can be tested using:

- Postman
- Thunder Client
- Browser Developer Tools

### Testing Areas
- Authentication Testing
- API Endpoint Validation
- Database Operations
- Authorization Testing
- UI Functionality Testing

---

# Team Contributions

| Team Member | Role | Contribution |
|-------------|------|--------------|
| Member 1 | Backend Developer | API Development & Authentication |
| Member 2 | Frontend Developer | UI Design & Integration |
| Member 3 | Database Engineer | Database Design & Query Management |
| Member 4 | QA & Documentation | Testing and Project Documentation |

> Replace placeholder names with actual contributor information.

---

# Academic Context

This project was developed as part of an academic coursework/project to demonstrate practical implementation of:

- Database Management Systems
- Software Engineering Principles
- REST API Development
- Authentication & Authorization
- Full Stack Web Development

---

# License

This repository is intended for **educational and academic purposes only**.

---

<div align="center">

### Smart Apartment Management System  
**Designed for efficient apartment administration and tenant management**

</div>
