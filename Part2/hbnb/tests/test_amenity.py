import unittest
from app import create_app

class TestAmenity(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.amenity_data = {"amenity_name": "WiFi"} 

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        
        if response.status_code != 201:
            self.fail(f"Amenity Failed: {response.json}")
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['amenity_name'], "WiFi")

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/') 
        self.assertEqual(response.status_code, 200)

    def test_get_amenity(self):
        post_response = self.client.post('/api/v1/amenities/', json=self.amenity_data)
        amenity_id = post_response.json['id']
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()