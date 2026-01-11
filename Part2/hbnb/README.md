# HBnB API (Part 2)

A layered REST-style API for an Airbnb-like domain: **Users, Places, Amenities, Bookings, Payments, Refunds, Reviews, Guests**, plus relationship entities and status/type enums.

---

## Overview

This project follows a clean layered architecture:

- **Models**: Domain entities + basic validation + shared `BaseModel` fields (e.g., `id`, timestamps).
- **Services**: Business logic (use-cases, rules, input validation, orchestration).
- **Persistence**: `Repository` abstraction for storing and retrieving entities (often in-memory for Part 2, but replaceable later).
- **Enums**: Centralized statuses/types for consistent state management.

---

## Project Structure

```txt
api/
├── __init__.py
├── v1/
├── enums/
│   ├── booking_status.py
│   ├── payment_status.py
│   ├── payment_type.py
│   ├── place_amenity_status.py
│   ├── place_status.py
│   └── refund_status.py
├── models/
│   ├── __init__.py
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
│   ├── __init__.py
│   └── repository.py
└── services/
    ├── __init__.py
    ├── facade.py
    ├── user_service.py
    ├── place_service.py
    ├── amenity_service.py
    ├── guest_service.py
    ├── booking_service.py
    ├── payment_service.py
    ├── refund_service.py
    └── review_service.py

Architecture Notes
Facade Pattern

services/facade.py is the single entry point used by the API layer to call business logic without touching repositories directly.

Typical flow:

API (v1 routes/controllers) → Facade → Service → Repository → Model

Repository Pattern

persistence/repository.py provides a consistent interface (implementation may vary):

add(entity)

get(entity_id)

update(entity)

delete(entity_id)

list() (optional)

This makes it easy to replace in-memory storage with a real database later.