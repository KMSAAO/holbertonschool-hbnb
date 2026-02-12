# 🏠 HBNB – API Testing & Validation Report

## 1. Introduction
This document presents a complete testing and validation report for the **HBNB API**.  
It describes the validation logic implemented in the service layer, the results of automated unit tests, and manual testing using `cURL` to ensure that all endpoints behave correctly.

---

## 2. Validation Logic

All validation rules are enforced in the **Service Layer** before persistence to guarantee data integrity.

### User Validation
- Email must be valid and unique
- First and last names are required and must not exceed 50 characters
- Password must be at least 6 characters long

### Place Validation
- Price must be a positive float
- Latitude must be between -90.0 and 90.0
- Longitude must be between -180.0 and 180.0
- Owner must reference an existing user

### Review Validation
- Rating must be an integer between 1 and 5
- Reviews cannot be created for non-existent places
- Reviews cannot be created by non-existent users

### Amenity Validation
- Name is required and must not exceed 50 characters
- Status must match allowed enum values (active, inactive, etc.)

---

## 3. Automated Unit Tests
```bash
python3 -m unittest discover tests -v
```
The following output confirms that all automated unit tests passed successfully:
```bash
test_create_amenity (test_amenity.TestAmenityAPI.test_create_amenity) ... ok
test_create_amenity_invalid_data (test_amenity.TestAmenityAPI.test_create_amenity_invalid_data) ... ok
test_delete_amenity (test_amenity.TestAmenityAPI.test_delete_amenity) ... ok
test_delete_amenity_not_found (test_amenity.TestAmenityAPI.test_delete_amenity_not_found) ... ok
test_get_amenity (test_amenity.TestAmenityAPI.test_get_amenity) ... ok
test_get_amenity_not_found (test_amenity.TestAmenityAPI.test_get_amenity_not_found) ... ok
test_update_amenity (test_amenity.TestAmenityAPI.test_update_amenity) ... ok
test_update_amenity_not_found (test_amenity.TestAmenityAPI.test_update_amenity_not_found) ... ok
test_create_place_invalid_data (test_place.TestPlaceAPI.test_create_place_invalid_data)
Test creating a place with invalid data (e.g. negative price) ... ok
test_create_place_invalid_owner (test_place.TestPlaceAPI.test_create_place_invalid_owner)
Test creating a place with non-existent owner_id ... ok
test_create_place_success (test_place.TestPlaceAPI.test_create_place_success)
Test creating a place with valid data ... ok
test_delete_place (test_place.TestPlaceAPI.test_delete_place)
Test deleting a place ... ok
test_get_place (test_place.TestPlaceAPI.test_get_place)
Test retrieving a place by ID ... ok
test_update_place (test_place.TestPlaceAPI.test_update_place)
Test updating place details ... ok
test_create_review (test_review.TestReviewAPI.test_create_review) ... ok
test_create_review_invalid_data (test_review.TestReviewAPI.test_create_review_invalid_data) ... ok
test_delete_review (test_review.TestReviewAPI.test_delete_review) ... ok
test_get_review_info (test_review.TestReviewAPI.test_get_review_info) ... ok
test_get_review_not_found (test_review.TestReviewAPI.test_get_review_not_found) ... ok
test_update_review (test_review.TestReviewAPI.test_update_review) ... ok
test_update_review_not_found (test_review.TestReviewAPI.test_update_review_not_found) ... ok
test_active_user (test_user.TestUserAPI.test_active_user) ... ok
test_delete_user_not_found (test_user.TestUserAPI.test_delete_user_not_found) ... ok
test_delete_user_success (test_user.TestUserAPI.test_delete_user_success) ... ok
test_delete_user_with_linked_place (test_user.TestUserAPI.test_delete_user_with_linked_place) ... ok
test_email_already_registered (test_user.TestUserAPI.test_email_already_registered) ... ok
test_email_format (test_user.TestUserAPI.test_email_format) ... ok
test_email_or_password_not_exists (test_user.TestUserAPI.test_email_or_password_not_exists) ... ok
test_email_validation (test_user.TestUserAPI.test_email_validation) ... ok
test_get_info (test_user.TestUserAPI.test_get_info) ... ok
test_length_of_password (test_user.TestUserAPI.test_length_of_password) ... ok
test_login (test_user.TestUserAPI.test_login) ... ok
test_name_length (test_user.TestUserAPI.test_name_length) ... ok
test_password_type (test_user.TestUserAPI.test_password_type) ... ok
test_register_user (test_user.TestUserAPI.test_register_user) ... ok
test_register_user_missing_fields (test_user.TestUserAPI.test_register_user_missing_fields) ... ok
test_update_non_existent_user (test_user.TestUserAPI.test_update_non_existent_user) ... ok
test_update_user_invalid_data (test_user.TestUserAPI.test_update_user_invalid_data) ... ok
test_update_user_success (test_user.TestUserAPI.test_update_user_success) ... ok

----------------------------------------------------------------------
Ran 39 tests in 0.286s

OK
```
---

## 4. Manual Testing (cURL)

### A) Users Endpoint – Create User
```bash
curl -X POST http://127.0.0.1:5050/api/v1/users/register \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword"
}'
```
```bash
{
    "id": "528bc4a8-3bcc-4bd6-8ab6-2be576abc633",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false,
    "is_active": true,
    "created_at": "2026-01-13 22:11:10.913651",
    "updated_at": "2026-01-13 22:11:10.913656"
}
```
### B) Amenities Endpoint – Create Amenity
```bash
curl -X POST http://127.0.0.1:5050/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{
  "amenity_name": "WiFi",
  "description": "High-speed internet",
  "status": "Active"
}'
```
```bash
{
    "id": "6835146c-8829-47af-a5eb-d16da2139eb2",
    "amenity_name": "WiFi",
    "description": "High-speed internet",
    "status": "Active"
}
```
### C) Places Endpoint – Create Place
```bash
curl -X POST http://127.0.0.1:5050/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Cozy Apartment",
  "description": "Nice place in the city center",
  "price": 100.0,
  "latitude": 34.0522,
  "longitude": -118.2437,
  "owner_id": "528bc4a8-3bcc-4bd6-8ab6-2be576abc633",
  "status": "available"
}'
```
```bash
{
    "id": "fcb9728f-29d6-45be-bc00-e92e574e058c",
    "owner_id": "528bc4a8-3bcc-4bd6-8ab6-2be576abc633",
    "title": "Cozy Apartment",
    "description": "Nice place in the city center",
    "price": 100.0,
    "status": "PlaceStatus.AVAILABLE",
    "latitude": 34.0522,
    "longitude": -118.2437,
    "created_at": "2026-01-13 22:16:47.177381",
    "updated_at": "2026-01-13 22:16:47.177386"
}
```
### D) Reviews Endpoint – Create Review
```bash
curl -X POST http://127.0.0.1:5050/api/v1/reviews/ -H "Content-Type: application/json" -d '{
  "place_id": "fcb9728f-29d6-45be-bc00-e92e574e058c",
  "user_id": "528bc4a8-3bcc-4bd6-8ab6-2be576abc633",
  "rating": 5,
  "comment": "Amazing place!"
}'
```
```bash
{
    "id": "b23e1398-e4a9-4870-8422-e238d9ddd2c8",
    "place_id": "fcb9728f-29d6-45be-bc00-e92e574e058c",
    "rating": 5,
    "comment": "Amazing place!"
}
```
### Invalid Rating (Edge Case)
```bash
curl -X POST http://127.0.0.1:5050/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{
  "place_id": "fcb9728f-29d6-45be-bc00-e92e574e058c",
  "rating": 6,
  "comment": "Invalid"
}'
```
```bash
{
  "message": "rating must be between 1 and 5"
}
```
### 5. Conclusion
All API endpoints have been successfully implemented and validated.

Validation rules are correctly enforced

Automated unit tests fully cover API behavior

Manual testing confirms real-world correctness

Proper HTTP status codes are returned (200, 201, 400, 404)

Swagger UI documentation is available when running the application.