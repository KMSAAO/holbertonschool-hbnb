import unittest
import urllib.request
import urllib.error
import json
import uuid

BASE_URL = "http://127.0.0.1:5000/api/v1"

class TestFlowEdit(unittest.TestCase):
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
        except urllib.error.HTTPError:
            pass
            
        # Login
        login_data = {"email": email, "password": self.password}
        req = urllib.request.Request(f"{BASE_URL}/auth/login", data=json.dumps(login_data).encode(), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode())
            token = res_json['access_token']
            
        # Get ID via GET /users (mocking self lookup)
        req = urllib.request.Request(f"{BASE_URL}/users", headers={'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req) as response:
            users = json.loads(response.read().decode())
            user_id = next((u['id'] for u in users if u['email'] == email), None)
            return user_id, token

    def create_place(self, token, title):
        data = {
            "title": title,
            "description": "Initial Description",
            "price": 100.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "number_of_rooms": 2,
            "max_guests": 4
        }
        req = urllib.request.Request(f"{BASE_URL}/places", data=json.dumps(data).encode(), headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        })
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    def update_place(self, token, place_id, data):
        req = urllib.request.Request(f"{BASE_URL}/places/{place_id}", data=json.dumps(data).encode(), headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }, method='PUT')
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    def delete_place(self, token, place_id):
        req = urllib.request.Request(f"{BASE_URL}/places/{place_id}", headers={
            'Authorization': f'Bearer {token}'
        }, method='DELETE')
        with urllib.request.urlopen(req) as response:
            return response.getcode()

    def get_place(self, place_id):
        req = urllib.request.Request(f"{BASE_URL}/places/{place_id}")
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    def test_authorized_edit_flow(self):
        """User A creates a place, edits it, and verifying updates persists."""
        # 1. Create
        place = self.create_place(self.token_a, "Original Title")
        place_id = place['id']
        self.assertEqual(place['title'], "Original Title")
        self.assertEqual(place['number_of_rooms'], 2)

        # 2. Update
        update_data = {
            "title": "Updated Title",
            "price": 150.0,
            "number_of_rooms": 5,
            "tagline": "Best place ever"
        }
        updated_place = self.update_place(self.token_a, place_id, update_data)
        self.assertEqual(updated_place['title'], "Updated Title")
        self.assertEqual(updated_place['price'], 150.0)
        self.assertEqual(updated_place['number_of_rooms'], 5)
        self.assertEqual(updated_place['tagline'], "Best place ever")

        # 3. Verify Persistence
        fetched_place = self.get_place(place_id)
        self.assertEqual(fetched_place['title'], "Updated Title")
        self.assertEqual(fetched_place['price'], 150.0)
        self.assertEqual(fetched_place['number_of_rooms'], 5)

    def test_unauthorized_edit(self):
        """User B tries to edit User A's place -> 403 Forbidden."""
        place = self.create_place(self.token_a, "User A Place")
        place_id = place['id']

        update_data = {"title": "Hacked Title"}
        
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.update_place(self.token_b, place_id, update_data)
        
        self.assertEqual(cm.exception.code, 403)

        # Verify not changed
        fetched_place = self.get_place(place_id)
        self.assertEqual(fetched_place['title'], "User A Place")

    def test_unauthorized_delete(self):
        """User B tries to delete User A's place -> 403 Forbidden."""
        place = self.create_place(self.token_a, "User A Place")
        place_id = place['id']
        
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.delete_place(self.token_b, place_id)
        
        self.assertEqual(cm.exception.code, 403)

        # Verify still exists
        fetched_place = self.get_place(place_id)
        self.assertIsNotNone(fetched_place)

    def test_delete_flow(self):
        """User A deletes their place -> Success -> 404 on Get."""
        place = self.create_place(self.token_a, "To Delete")
        place_id = place['id']

        # Delete
        code = self.delete_place(self.token_a, place_id)
        self.assertEqual(code, 200)

        # Verify 404
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.get_place(place_id)
        
        self.assertEqual(cm.exception.code, 404)

if __name__ == '__main__':
    unittest.main()
