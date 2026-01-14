# HBnB Evolution: Part 2 - Implementation of Business Logic & API Endpoints 🏨
Welcome to the implementation phase of the HBnB Project. In this part, we have transformed our architectural designs into a functional RESTful API using Python and Flask, focusing on modularity, the Facade Design Pattern, and strict separation of concerns.

# 🎯 Project Vision
The goal of this phase was to build a robust foundation for the HBnB application, implementing the Presentation and Business Logic layers. We prioritized clean code, data validation, and a scalable project structure to prepare for future integration with a persistent database (SQLAlchemy) and JWT authentication.

# 🏗 Modular Architecture

- The project is organized into a three-layer architecture to ensure maintainability:

- Presentation Layer (API): Built with Flask-RESTX to handle HTTP requests and document the API with Swagger.

- Business Logic Layer: Defines the core entities (User, Place, Review, Amenity) and their relationships.

- Persistence Layer: Currently utilizes an In-Memory Repository (Object Storage) for rapid prototyping, designed to be easily swapped with a database in Part 3.

# 🔑 Key Design Pattern: The Facade
We implemented the Facade Pattern to simplify the interaction between the API Endpoints and the Business Logic. This ensures that the Presentation layer doesn't need to know the complexities of how objects are stored or validated.

# ✨ Features Implemented 

### 1. Core Entities & OOP
Implemented the base classes and concrete models using Python OOP:

- UUID4: Used for secure and unique identification of all objects.

- Attributes: Managed created_at and updated_at timestamps for all entities.

- Validation: Strict validation for email formats, price ranges, and geographical coordinates (Latitude/Longitude).

### 2. RESTful API Endpoints
We developed comprehensive endpoints for managing the system:

- Users: Create and Update profiles, and retrieve user data (passwords are strictly excluded from responses).

- Amenities: Full CRUD operations (excluding Delete) to manage property features.

- Places: Complex endpoint handling relationships between Owners (Users) and Amenities.

- Reviews: Comprehensive management, including the ability to link reviews to specific places and users. (Note: Delete operation is supported for Reviews).

### 3. Data Serialization
Implemented advanced serialization to return nested data. For example, when fetching a Place, the API returns:
- Owner details (First Name, Last Name).

- A list of associated Amenities.

- A list of Reviews (updated in Task 5).


# 🛠 Tech Stack

- Language: Python 3.x

- Web Framework: Flask

- API Documentation: Flask-RESTX (Swagger)

- Testing Tools: Unittest, cURL, Postman

# 🧪 Testing & Validation

Quality assurance was a priority for this sprint:

- Unit Testing: Automated tests using the unittest framework to validate business logic.

- Black-box Testing: Conducted via cURL and Postman to ensure endpoints return correct status codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found).

- Swagger: Used for real-time API testing and documentation.

## Project Structure

```txt
api/
├── _init_.py
├── v1/
├── enums/
│   ├── booking_status.py
│   ├── payment_status.py
│   ├── payment_type.py
│   ├── place_amenity_status.py
│   ├── place_status.py
│   └── refund_status.py
├── models/
│   ├── _init_.py
│   ├── base_model.py
│   ├── user.py
│   ├── guest.py
│   ├── place.py
│   ├── amenity.py
│   ├── place_amenity.py
│   ├── booking.py
│   ├── payment.py
│   ├── refund.py
│   └── review.py
├── persistence/
│   ├── _init_.py
│   └── repository.py
└── services/
    ├── _init_.py
    ├── facade.py
    ├── user_service.py
    ├── place_service.py
    ├── amenity_service.py
    ├── guest_service.py
    ├── booking_service.py
    ├── payment_service.py
    ├── refund_service.py
    └── review_service.py
```
# 📂 Structure Notes

Note on Modular Service Design: > Our architecture goes beyond a basic Flask setup by implementing a dedicated Service Layer (api/services/).

Service Orchestration: Each entity (User, Place, Booking, etc.) has its own dedicated service to handle specific business logic and data validation.

Separation of Concerns: This structure ensures that the facade.py remains clean and high-level, delegating specialized tasks to the respective service modules.

Scalability: By isolating enums and models, the system is prepared for complex state management (e.g., Booking and Payment statuses) and easy extension of business rules.

# 👥 Authors & Collaboration
- Nawaf Alzahrani
- Khalid Alomari
- Shatha Alsuwailm
