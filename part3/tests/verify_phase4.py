import unittest
import urllib.request
import json
import uuid

BASE_URL = "http://127.0.0.1:5000/api/v1"

class TestPhase4(unittest.TestCase):
    def setUp(self):
        self.user_a_email = f"user_a_{uuid.uuid4()}@test.com"
        self.user_b_email = f"user_b_{uuid.uuid4()}@test.com"
        self.password = "123456"
        
        # Create Users
        self.user_a_id, self.token_a = self.create_and_login(self.user_a_email, "User", "A")
        self.user_b_id, self.token_b = self.create_and_login(self.user_b_email, "User", "B")

    def create_and_login(self, email, first, last):
        # Register
        data = {
            "email": email,
            "first_name": first,
            "last_name": last,
            "password": self.password
        }
        req = urllib.request.Request(f"{BASE_URL}/users", data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as response:
                pass
        except urllib.error.HTTPError as e:
            # Maybe already exists
            pass
            
        # Login
        login_data = {"email": email, "password": self.password}
        req = urllib.request.Request(f"{BASE_URL}/auth/login", data=json.dumps(login_data).encode(), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode())
            token = res_json['access_token']
            
        # Get ID
        req = urllib.request.Request(f"{BASE_URL}/users", headers={'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req) as response:
            # This returns all users? Or we need to find self.
            # actually we can just extract from token if we decoded it, but let's assume we can fetch places created later.
            # Let's just return token and we will get ID from creating a place? 
            # Or use GET /users and find by email
            users = json.loads(response.read().decode())
            user_id = next((u['id'] for u in users if u['email'] == email), None)
            return user_id, token

    def create_place(self, token, title):
        data = {
            "title": title,
            "description": "Desc",
            "price": 100.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": "ignored_backend_uses_token_or_payload?" 
            # Wait, PlacesAPI.create uses payload user_id?
            # In update admin.js: user_id: userId
        }
        # Ideally backend should fallback to token identity if user_id not provided, 
        # but PlaceService.create_place takes user_id from payload or arguments.
        # Let's check api/v1/places.py post method.
        # It expects `place_create_model`.
        # It calls `facade.create_place(api.payload)`.
        # `place_create_model` has no user_id?
        # Let's check.
        pass

    def test_filter_by_user(self):
        print(f"User A ID: {self.user_a_id}")
        
        # Create 2 places for A
        p1 = self.create_place_real(self.token_a, self.user_a_id, "Place A1")
        print(f"Created P1: {p1['id']}, owner: {p1.get('owner_id')}")
        p2 = self.create_place_real(self.token_a, self.user_a_id, "Place A2")
        print(f"Created P2: {p2['id']}, owner: {p2.get('owner_id')}")
        
        # Create 1 place for B
        p3 = self.create_place_real(self.token_b, self.user_b_id, "Place B1")
        print(f"Created P3: {p3['id']}, owner: {p3.get('owner_id')}")
        
        # Get places for A
        places_a = self.get_places(user_id=self.user_a_id)
        print(f"Places for User A: {len(places_a)}")
        self.assertEqual(len(places_a), 2)
        self.assertTrue(all(p['title'].startswith("Place A") for p in places_a))
        
        # Get places for B
        places_b = self.get_places(user_id=self.user_b_id)
        print(f"Places for User B: {len(places_b)}")
        self.assertEqual(len(places_b), 1)
        self.assertEqual(places_b[0]['title'], "Place B1")
        
        # Get places for ME (as A)
        places_me_a = self.get_places(token=self.token_a, user_id='ME')
        print(f"Places for ME (A): {len(places_me_a)}")
        self.assertEqual(len(places_me_a), 2)

    def create_place_real(self, token, user_id, title):
        data = {
            "title": title,
            "description": "Test Desc",
            "price": 50,
            "latitude": 0,
            "longitude": 0,
            "user_id": user_id, # Backend needs this if not using token identity for creation
            "owner_id": user_id 
        }
        req = urllib.request.Request(f"{BASE_URL}/places", data=json.dumps(data).encode(), headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        })
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    def get_places(self, user_id=None, token=None):
        url = f"{BASE_URL}/places"
        if user_id:
            url += f"?user_id={user_id}"
        
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
            
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

if __name__ == '__main__':
    unittest.main()
