import unittest
import uuid
from app import create_app

class TestAmenityAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.amenity_data = {
            "amenity_name": "WiFi",
            "description": "High speed internet",
            "status": "Active"
        }

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['amenity_name'], self.amenity_data['amenity_name'])
        self.assertEqual(response.json['description'], self.amenity_data['description'])

    def test_create_amenity_invalid_data(self):
        invalid_data = {
            "description": "Missing name"
        }
        response = self.client.post('/api/v1/amenities/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_get_amenity(self):
        create_response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        amenity_id = create_response.json['id']

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], amenity_id)
        self.assertEqual(response.json['amenity_name'], self.amenity_data['amenity_name'])

    def test_get_amenity_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/amenities/{fake_id}')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        create_response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        amenity_id = create_response.json['id']

        update_data = {
            "amenity_name": "Super WiFi",
            "status": "Disabled"
        }
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['amenity_name'], "Super WiFi")
        self.assertEqual(response.json['status'], "Disabled")
        self.assertEqual(response.json['description'], self.amenity_data['description'])

    def test_update_amenity_not_found(self):
        fake_id = str(uuid.uuid4())
        update_data = {"amenity_name": "Ghost Amenity"}
        response = self.client.put(f'/api/v1/amenities/{fake_id}', json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        create_response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        amenity_id = create_response.json['id']

        response = self.client.delete(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 204)

        get_response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_amenity_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.delete(f'/api/v1/amenities/{fake_id}')
        self.assertEqual(response.status_code, 404)