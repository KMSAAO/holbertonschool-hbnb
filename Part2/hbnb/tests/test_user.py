import unittest
import uuid
from app import create_app

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test_{uuid.uuid4()}@example.com",
            "password": "password123",
            "is_admin": False
        }

    def test_register_user(self):
        """Test creating a new user"""
        response = self.client.post('/api/v1/users/register', json=self.user_data)
        
        if response.status_code != 201:
            self.fail(f"User Registration Failed with: {response.json}")
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['email'], self.user_data['email'])


    def test_register_existing_email(self):
        """Test registering with an existing email (should fail)"""
        self.client.post('/api/v1/users/register', json=self.user_data)
        response = self.client.post('/api/v1/users/register', json=self.user_data)
        self.assertEqual(response.status_code, 400)

    def test_login_user(self):
        """Test user login"""
        self.client.post('/api/v1/users/register', json=self.user_data)
        
        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }
        response = self.client.post('/api/v1/users/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Login successful')

if __name__ == '__main__':
    unittest.main()