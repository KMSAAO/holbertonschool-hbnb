import unittest
import uuid
from app import create_app

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        unique_email = f"owner_{uuid.uuid4()}@test.com"
        
        user_data = {
            "first_name": "Owner",
            "last_name": "One",
            "email": unique_email,
            "password": "password123"
        }
        user_response = self.client.post('/api/v1/users/register', json=user_data)
        
        if user_response.status_code != 201:
            raise ValueError(f"Failed to create owner: {user_response.json}")

        self.owner_id = user_response.json['id']

        self.place_data = {
            "title": "Cozy Apartment",
            "description": "Nice place",
            "price": 100.0,
            "status": "available",
            "latitude": 30.0,
            "longitude": 30.0,
            "owner_id": self.owner_id
        }

    def test_create_place(self):
        """Test creating a place linked to a user"""
        response = self.client.post('/api/v1/places/', json=self.place_data)
        
        if response.status_code != 201:
            self.fail(f"Place Creation Failed: {response.json}")
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], "Cozy Apartment")
    def test_create_place_invalid_owner(self):
        self.place_data['owner_id'] = "invalid_id"
        response = self.client.post('/api/v1/places/', json=self.place_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()