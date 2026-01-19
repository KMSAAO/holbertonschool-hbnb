import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app.services.guest_service import GuestService
from app.models.user import User
from app.models.guest import Guest
from app.persistence.repository import InMemoryRepository

class TestGuestService(unittest.TestCase):
    def setUp(self):
        self.service = GuestService()
        self.repo = InMemoryRepository()
        
        self.valid_user = User(
            first_name="Nawaf",
            last_name="Alzahrani",
            email="nawaf@example.com",
            password="123456"
        )
        self.repo.add(self.valid_user)  # ✅ استخدم add بدل save

        self.valid_user_id = self.valid_user.id
        self.valid_data = {"bio": "I love traveling"}

    def test_register_guest_success(self):
        guest = self.service.register_as_guest(self.valid_user_id, self.valid_data, self.repo)
        self.assertIsInstance(guest, Guest)
        self.assertEqual(guest.bio, self.valid_data["bio"])
        self.assertEqual(guest.user.id, self.valid_user_id)

    def test_register_guest_missing_user_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.service.register_as_guest(None, self.valid_data, self.repo)
        self.assertIn("user_id is required", str(ctx.exception))

    def test_register_guest_invalid_bio_type(self):
        with self.assertRaises(ValueError) as ctx:
            self.service.register_as_guest(self.valid_user_id, {"bio": 12345}, self.repo)
        self.assertIn("bio is required and must be a string", str(ctx.exception))

    def test_register_guest_long_bio(self):
        long_bio = "A" * 101
        with self.assertRaises(ValueError) as ctx:
            self.service.register_as_guest(self.valid_user_id, {"bio": long_bio}, self.repo)
        self.assertIn("bio is required and must be a string with max 100 characters", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
