import unittest
import uuid
from app import create_app

class TestUserAPI(unittest.TestCase):
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

        self.response = self.client.post('/api/v1/users/register', json=self.user_data)

        self.user_id = self.response.json['id']
    def test_register_user(self):

        if self.response.status_code != 201:
            self.fail(f"User registration failed: {self.response.json}")

            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json)
            self.assertEqual(response.json['email'], self.user_data['email'])

    def test_email_already_registered(self):
        response1 = self.client.post('/api/v1/users/register', json=self.user_data)
        self.assertEqual(response1.status_code, 400)
        self.assertIn('Email already registered', response1.json['message'])

    def test_register_user_missing_fields(self):
        incomplete_data = self.user_data.copy()
        del incomplete_data['email']

        response1 = self.client.post('/api/v1/users/register', json=incomplete_data)

        self.assertEqual(response1.status_code, 400)
        self.assertIn('Input payload validation failed', response1.json['message'])


    def test_email_format(self): 
        invalid_email_data = self.user_data.copy()
        invalid_email_data['email'] = 'kh.com'

        response1 = self.client.post('/api/v1/users/register', json=invalid_email_data)

        self.assertEqual(response1.status_code, 400)
        self.assertIn('Invalid email format', response1.json['message'])

    def test_length_of_password(self):
        length_password = self.user_data.copy()
        length_password['password'] = '12345'
        length_password['email'] = 'email@gg.com'

        response1 = self.client.post('/api/v1/users/register', json=length_password)

        self.assertEqual(response1.status_code, 400)
        self.assertIn("Password must be at least 6 characters", response1.json['message'])

    def test_name_length(self):
        max_name_data = self.user_data.copy()
        max_name_data['first_name'] = "k" * 51
        max_name_data['email'] = 'email@gg.com'

        response1 = self.client.post('/api/v1/users/register', json=max_name_data)

        self.assertEqual(response1.status_code, 400)
        self.assertIn('First name is required and must be a string with max 50 characters', response1.json['message'])
    # TEST LOGIN
    def test_login(self):
        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }

        response1 = self.client.post('/api/v1/users/login', json=login_data)
        if response1.status_code != 200:
            self.fail(f"Login failed: {response1.json}")

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json['message'], 'Login successful')

    def test_email_validation(self):
        login_data = {
            "email": 'nawaf.com',
            "password": self.user_data['password']
        }
        response = self.client.post('/api/v1/users/login', json=login_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Valid email is required', response.json['message'])
    
    def test_password_type(self):
        login_data = {
            "email": 'nawaf@shatha.com',
            "password": 214325
        }
                
        response1 = self.client.post('/api/v1/users/login', json=login_data)

        self.assertEqual(response1.status_code, 400)
        self.assertIn('Input payload validation failed', response1.json['message'])
    
    def test_email_or_password_not_exists(self):

        login_data = {
            "email": 'khalid@aa.com',
            "password": self.user_data['password']
        }

        response = self.client.post('/api/v1/users/login', json=login_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(response.json['message'], 'Incorrect email or password')

    def test_active_user(self):
        user_not_active = self.user_data
        user_not_active['email'] = 'kj@gg.com'
        user_not_active['is_active'] = False
        self.client.post('/api/v1/users/register', json=self.user_data)

        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password'],
        }

        response = self.client.post('/api/v1/users/login', json=login_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn(response.json['message'], 'User is not active')
    #TEST GET USER INFO
    def test_get_info(self):
            response = self.client.get(f"/api/v1/users/{self.user_id}")
            
            self.assertEqual(response.status_code, 200)
            
            data = response.json

            self.assertEqual(data['id'], self.user_id)
            self.assertEqual(data['first_name'], self.user_data['first_name'])
            self.assertEqual(data['last_name'], self.user_data['last_name'])
            self.assertEqual(data['email'], self.user_data['email'])
            self.assertIn('created_at', data)
            self.assertIn('updated_at', data)

            self.assertIsInstance(data['created_at'], str)
            self.assertIsInstance(data['updated_at'], str)

    def test_update_user_success(self):
            update_payload = {
                "first_name": "UpdatedName",
                "password": "newpassword123"
            }

            response = self.client.put(f'/api/v1/users/{self.user_id}', json=update_payload)

            self.assertEqual(response.status_code, 200)
            get_response = self.client.get(f'/api/v1/users/{self.user_id}')
            self.assertEqual(get_response.json['first_name'], "UpdatedName")
            self.assertEqual(response.json['email'], self.user_data['email'])
            self.assertEqual(response.json['id'], self.user_id)

    def test_update_user_invalid_data(self):
            invalid_payload = {
                "password": "123"
            }
            response = self.client.put(f'/api/v1/users/{self.user_id}', json=invalid_payload)
            
            self.assertEqual(response.status_code, 400)
            self.assertIn('Password must be at least 6 characters', response.json['message'])

            long_name_payload = {
                "first_name": "a" * 51 
            }
            response = self.client.put(f'/api/v1/users/{self.user_id}', json=long_name_payload)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid first name', response.json['message'])


    def test_update_non_existent_user(self):
            import uuid
            fake_id = str(uuid.uuid4())
            
            update_payload = {"first_name": "Ghost"}
            
            response = self.client.put(f'/api/v1/users/{fake_id}', json=update_payload)
            
            self.assertEqual(response.status_code, 404) 
            self.assertIn('User not found', response.json['message'])


    def test_delete_user_success(self):
        response = self.client.delete(f'/api/v1/users/{self.user_id}')
        
        self.assertEqual(response.status_code, 204)
        
        get_response = self.client.get(f'/api/v1/users/{self.user_id}')
        self.assertEqual(get_response.status_code, 404)



    def test_delete_user_not_found(self):
        fake_id = str(uuid.uuid4())
        
        response = self.client.delete(f'/api/v1/users/{fake_id}')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.json['message'])


    def test_delete_user_with_linked_place(self):        
        place_data = {
            "title": "My House",
            "description": "Lovely place",
            "price": 100,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
            "status": "available"
        }
        place_response = self.client.post('/api/v1/places/', json=place_data)
        if place_response.status_code != 201:
            self.fail(f"Failed to create place: {place_response.json}")
        
        response = self.client.delete(f'/api/v1/users/{self.user_id}')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Cannot delete user with existing places', response.json['message'])


if __name__ == '__main__':
    unittest.main()