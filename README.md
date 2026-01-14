# HBnB Evolution: Full-Stack Backend Service 🏨

### 🌟 Project Overview
HBnB Evolution is a comprehensive AirBnB-like application designed to manage a marketplace of property listings, user interactions, and booking experiences. 

This project follows a strict evolutionary development process—moving from architectural design to a secure, database-backed production system.

The system allows users to register, list properties (Places), manage amenities, and provide feedback through a robust review system.


### 🛠 Project Phases & Evolution
### Part 1: Technical Documentation & Design
The foundation of the project was built on solid UML standards:

- Architecture: Layered design (Presentation, Business Logic, Persistence).

- Diagrams: High-level Package diagrams, detailed Class diagrams for Business Logic, and Sequence diagrams for API flows (Registration, Place creation, etc.).

### Part 2: Business Logic & API Implementation
Transformation of designs into a functional Flask-based RESTful API:
- Facade Pattern: Implemented a central service layer to decouple the API from the models.

- Modular Design: Introduction of dedicated services and enums for state management.

- In-Memory Storage: Initial prototyping using a flexible repository pattern.

### Part 3: Security & Database Persistence (Current State)
Scaling the application for real-world deployment:

- Authentication: Secure JWT-based sessions using Flask-JWT-Extended.

- Authorization: Role-Based Access Control (RBAC) ensuring only administrators can perform sensitive operations.

- Database Integration: Transitioned from in-memory storage to SQLite (for development) and MySQL (for production) using SQLAlchemy ORM.

- Security: Password hashing using bcrypt.

# 🏛 Architecture & Engineering Notes

### The Facade & Service Layers

To ensure the Single Responsibility Principle, we structured the backend as follows:

API (Flask-RESTX) ➔ Facade (Entry Point) ➔ Specialized Services ➔ SQLAlchemy ORM ➔ Database

Persistence Layer

By utilizing the Repository Pattern, we achieved "Storage Agility."
We can switch the entire database backend by modifying the persistence configuration without touching a single line of business logic.

# 🚀 Key Features

- User Management: Secure registration, profile updates, and admin roles.

- Place Listing: Detailed property management (Price, Location, Amenities).

- Review System: Complete CRUD for user feedback and ratings.

- Advanced Search: Fetching places with nested details (Owner info & Amenities).

- Secure API: Protected endpoints requiring valid JWT tokens.

