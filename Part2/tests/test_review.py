import unittest
import uuid
from app import create_app

class TestReviewAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()        

        unique_email = f"owner_{uuid.uuid4()}@test.com"

        self.user_data = {
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email,
            "password": "password123"
        }
        
        user_response = self.client.post('/api/v1/users/register', json=self.user_data)
        
        if user_response.status_code != 201:
            raise ValueError(f"Setup failed: Could not create user. Status: {user_response.status_code}, Response: {user_response.json}")

        self.owner_id = user_response.json['id']

        self.place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 34.05,
            "longitude": -118.25,
            "owner_id": self.owner_id,
            "status": "available" 
        }

        place_response = self.client.post('/api/v1/places/', json=self.place_data)

        if place_response.status_code != 201:
            raise ValueError(f"Setup failed: Could not create place. Status:{place_response.status_code}, Response: {place_response.json}")
        
        self.place_id = place_response.json['id']

        
        self.review_data = {
            "place_id": self.place_id,
            "rating": 4,
            "comment":"this place is great"
        }




    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json=self.review_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['rating'], self.review_data['rating'])
        self.assertEqual(response.json['comment'], self.review_data['comment'])
        self.assertEqual(response.json['place_id'], self.review_data['place_id'])
        self.place_id = response.json['id']


    def test_create_review_invalid_data(self):
        invalid_data = self.review_data.copy()
        invalid_data['rating'] = 6

        response = self.client.post('/api/v1/reviews/', json=invalid_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual('rating must be between 0 to 5', response.json['message'])

    def test_get_review_info(self):
        response = self.client.post('/api/v1/reviews/', json=self.review_data)
        review_id = response.json['id']

        getrev = self.client.get(f"/api/v1/reviews/{review_id}")

        self.assertEqual(getrev.status_code, 200)
        self.assertEqual(getrev.json['comment'], self.review_data['comment'])
        self.assertEqual(getrev.json['id'], review_id)
    

    def test_update_review(self):
        create_response = self.client.post('/api/v1/reviews/', json=self.review_data)
        review_id = create_response.json['id']

        update_data = {
            "rating": 5,
            "comment": "Updated comment: Simply amazing!"
        }

        response = self.client.put(f'/api/v1/reviews/{review_id}', json=update_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['rating'], 5)
        self.assertEqual(response.json['comment'], "Updated comment: Simply amazing!")
        self.assertEqual(response.json['id'], review_id)

    def test_delete_review(self):
        create_response = self.client.post('/api/v1/reviews/', json=self.review_data)
        review_id = create_response.json['id']

        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        
        self.assertEqual(response.status_code, 204)

        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_get_review_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/reviews/{fake_id}')
        self.assertEqual(response.status_code, 404)

    def test_update_review_not_found(self):
        fake_id = str(uuid.uuid4())
        
        update_data = {
            "rating": 5,
            "comment": "This update should fail"
        }
        response = self.client.put(f'/api/v1/reviews/{fake_id}', json=update_data)

        self.assertEqual(response.status_code, 404)        
        self.assertIn("Review not found", response.json.get('message', ''))