import unittest
import uuid
from app import create_app

class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = f"reviewer_{uuid.uuid4()}@test.com"
        user_resp = self.client.post('/api/v1/users/register', json={
            "first_name": "Reviewer", "last_name": "Guy", 
            "email": unique_email, "password": "password123"
        })
        self.user_id = user_resp.json['id']

        owner_email = f"owner_place_{uuid.uuid4()}@test.com"
        owner_resp = self.client.post('/api/v1/users/register', json={
            "first_name": "Owner", "last_name": "P", 
            "email": owner_email, "password": "password123"
        })
        owner_id = owner_resp.json['id']

        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Test Place", 
            "price": 50, 
            "latitude": 10, 
            "longitude": 10, 
            "owner_id": owner_id,
            "status": "available"
        })
        
        if place_resp.status_code != 201:
            raise ValueError(f"Failed to create place: {place_resp.json}")
            
        self.place_id = place_resp.json['id']

        self.review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json=self.review_data)
        if response.status_code != 201:
            print(f"DEBUG REVIEW ERROR: {response.json}")
        self.assertEqual(response.status_code, 201)

    def test_get_reviews_by_place(self):
        self.client.post('/api/v1/reviews/', json=self.review_data)
        response = self.client.get(f'/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()