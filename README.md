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

## Authentication & Authorization

- User Registration
- Login Authentication
- Role-Based Authorization
- Session/Token-Based Authentication

### Roles
| Role | Access |
|------|--------|
| Admin | Full Access |
| Tenant | Limited Access |

---

## User Management

- Create Users
- Update Users
- Delete Users
- View Users

---

## Apartment Management

- Apartment Allocation
- Apartment Tracking
- Status Management

---

## Bill Management

- Bill Generation
- Bill Tracking
- Payment Monitoring

---

## Service Requests

- Maintenance Requests
- Priority Handling
- Status Tracking

---

## Dashboard

- Overview of Users
- Apartments
- Bills
- Activities

---

# System Architecture

Frontend → Flask API → MySQL Database

---

# Technology Stack

- Python
- Flask
- MySQL
- HTML, CSS, Bootstrap
- JavaScript
- bcrypt

---

# Project Structure

```
Smart_Apartment_Sustem/
│── Backend/
│   ├── app.py
│   ├── config.py
│   └── users.py
│
│── Frontend/
│   └── users.html
│
│── dashboard.html
│── apartment.html
│── Billtable.html
│── models.py
│── requirements.txt
│── README.md
│── env.txt
```

---

# Installation & Setup

## 1. Clone Repository
```
git clone https://github.com/your-username/Smart_Apartment_Sustem.git
cd Smart_Apartment_Sustem
```

## 2. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate (Linux/Mac)
```

## 3. Install Dependencies
```
pip install -r requirements.txt
```

---

# Database Configuration

```
CREATE DATABASE smart_apartment;
```

Update `config.py`:
```
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "smart_apartment"
DB_PORT = 3306
```

---

# Running the Application

```
python app.py
```

Open:
```
http://localhost:5000
```

---

# API Documentation

## Auth
- POST `/api/auth/register`
- POST `/api/auth/login`

## Users
- GET `/api/users`
- POST `/api/users`
- GET `/api/users/<id>`
- PUT `/api/users/<id>`
- DELETE `/api/users/<id>`

## Bills
- GET `/api/bills`
- POST `/api/bills`

---

# Security Features

- Role-Based Access Control
- Token Authentication
- Password Encryption (bcrypt)
- Protected Routes
- Error Handling

---

# Future Enhancements

- Online Payment System
- Mobile App
- SMS/Email Notifications
- AI-Based Monitoring
- Real-time Tracking

---

# Testing

- Postman
- Thunder Client
- Browser Dev Tools

---

# Team Contributions

The Smart Apartment Management System was developed collaboratively by a team where each member was responsible for a specific module of the project.

| Team Member | Student ID | Responsibility / Contribution |
|-------------|------------|--------------------------------|
| **Md. Abu Houraira Fahad** | **2023200000090** | Designed and developed the **Apartment Management Module**, including apartment-related functionalities and management features. |
| **Shahriar Sabbir** | **2023200000210** | Developed the **User Table and User Management Module**, including tenant/user-related operations. |
| **Rahad Hossen** | **2023200000332** | Designed and implemented the **Bills Table and Billing Management Module** for bill tracking and management. |
| **Md. Parvez Hossen** | **2023200000266** | Developed the **Visitor Table and Visitor Management Module** to manage visitor-related records and activities. |
| **Sumaya Akter Shumi** | **2023200000262** | Worked on the **Service Request and Activity Management Modules**, including maintenance services and activity tracking functionalities. |

### Additional Notes
Some supporting components, design references, and implementation ideas were adapted from **open-source resources and publicly available references** for learning and educational purposes. All modifications and integrations were performed to align with the project requirements.

---

# Academic Context

This project demonstrates:
- Database Design
- Web Development
- API Integration
- Authentication Systems
- Full Stack Development

---

# License

This project is for **educational purposes only**.
