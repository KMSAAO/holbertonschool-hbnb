import unittest
import uuid
from app import create_app

class TestReviewAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()        

        # 1. Create Owner User
        self.owner_email = f"owner_{uuid.uuid4()}@test.com"
        self.owner_data = {
            "first_name": "Owner",
            "last_name": "User",
            "email": self.owner_email,
            "password": "password123"
        }
        owner_resp = self.client.post('/api/v1/users', json=self.owner_data)
        self.owner_id = owner_resp.json['id']

        # 2. Login Owner to get token (needed to create place)
        owner_login = self.client.post('/api/v1/auth/login', json={
            "email": self.owner_email,
            "password": "password123"
        })
        self.owner_token = owner_login.json['access_token']
        self.owner_headers = {"Authorization": f"Bearer {self.owner_token}"}

        # 3. Create Place (owned by Owner)
        self.place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 34.05,
            "longitude": -118.25,
            "owner_id": self.owner_id,
            "status": "available" 
        }
        place_resp = self.client.post('/api/v1/places/', json=self.place_data, headers=self.owner_headers)
        self.place_id = place_resp.json['id']

        # 4. Create Reviewer User
        self.reviewer_email = f"reviewer_{uuid.uuid4()}@test.com"
        self.reviewer_data = {
            "first_name": "Reviewer",
            "last_name": "User",
            "email": self.reviewer_email,
            "password": "password123"
        }
        reviewer_resp = self.client.post('/api/v1/users', json=self.reviewer_data)
        self.reviewer_id = reviewer_resp.json['id']

        # 5. Login Reviewer to get token
        reviewer_login = self.client.post('/api/v1/auth/login', json={
            "email": self.reviewer_email,
            "password": "password123"
        })
        self.reviewer_token = reviewer_login.json['access_token']
        self.reviewer_headers = {"Authorization": f"Bearer {self.reviewer_token}"}

        # Standard Review Data
        self.review_data = {
            "place_id": self.place_id,
            "rating": 4,
            "comment": "This place is great"
        }

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['rating'], self.review_data['rating'])
        self.assertEqual(response.json['comment'], self.review_data['comment'])
        self.assertEqual(response.json['place_id'], self.review_data['place_id'])

    def test_create_review_invalid_rating(self):
        invalid_data = self.review_data.copy()
        invalid_data['rating'] = 6
        response = self.client.post('/api/v1/reviews/', json=invalid_data, headers=self.reviewer_headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating must be between 1 and 5', response.json['message'])

    def test_get_review_info(self):
        # Create
        create_resp = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        review_id = create_resp.json['id']

        # Get
        response = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['comment'], self.review_data['comment'])
        self.assertEqual(response.json['id'], review_id)

    def test_update_review_persistence(self):
        """Verify that updates are persisted to the database"""
        # Create
        create_resp = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        review_id = create_resp.json['id']

        # Update
        update_data = {
            "rating": 5,
            "comment": "Updated comment: Simply amazing!"
        }
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data, headers=self.reviewer_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['rating'], 5)

        # Verify Persistence by fetching again
        get_resp = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json['rating'], 5)
        self.assertEqual(get_resp.json['comment'], "Updated comment: Simply amazing!")

    def test_delete_review(self):
        create_resp = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        review_id = create_resp.json['id']

        # Delete
        response = self.client.delete(f'/api/v1/reviews/{review_id}', headers=self.reviewer_headers)
        self.assertEqual(response.status_code, 204)

        # Verify deletion
        get_resp = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_resp.status_code, 404)

    def test_review_own_place_forbidden(self):
        """Owner trying to review their own place should fail"""
        response = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.owner_headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("You cannot review your own place", response.json['message'])

    def test_duplicate_review_forbidden(self):
        """User cannot review the same place twice"""
        # First review
        response1 = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        self.assertEqual(response1.status_code, 201)

        # Second review attempt
        response2 = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        self.assertEqual(response2.status_code, 400)
        self.assertIn("You have already reviewed this place", response2.json['message'])

    def test_delete_review_unauthorized(self):
        """User cannot delete another user's review"""
        # Create review as Reviewer
        create_resp = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        review_id = create_resp.json['id']

        # Try to delete as Owner (who is just another user in this context, not the reviewer)
        response = self.client.delete(f'/api/v1/reviews/{review_id}', headers=self.owner_headers)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Unauthorized action", response.json['message'])

    def test_update_review_unauthorized(self):
        """User cannot update another user's review"""
        # Create review as Reviewer
        create_resp = self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)
        review_id = create_resp.json['id']

        # Try to update as Owner
        update_data = {"rating": 1, "comment": "Hacked review"}
        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data, headers=self.owner_headers)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Unauthorized action", response.json['message'])

    def test_delete_review_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.delete(f'/api/v1/reviews/{fake_id}', headers=self.reviewer_headers)
        self.assertEqual(response.status_code, 404)

    def test_place_reviews_include_user_details(self):
        """Verify that fetching place info includes reviews with user details (regression test)"""
        # Create review
        self.client.post('/api/v1/reviews/', json=self.review_data, headers=self.reviewer_headers)

        # Fetch place info
        response = self.client.get(f'/api/v1/places/{self.place_id}')
        self.assertEqual(response.status_code, 200)
        
        data = response.json
        self.assertTrue('reviews' in data)
        self.assertGreater(len(data['reviews']), 0)
        
        review = data['reviews'][0]
        self.assertTrue('user' in review)
        self.assertIsNotNone(review['user'])
        self.assertEqual(review['user']['first_name'], self.reviewer_data['first_name'])
        self.assertEqual(review['user']['last_name'], self.reviewer_data['last_name'])
        
        # Security check: Ensure email/password are NOT present
        self.assertNotIn('email', review['user'], "Email should not be exposed in review user details")
        self.assertNotIn('password', review['user'], "Password should not be exposed in review user details")