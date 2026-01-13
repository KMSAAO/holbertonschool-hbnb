import unittest
from app.models.guest import guest
from app.services.guest_service import GuestService

class FakeRepo:
    def __init__(self):
        self.storage = []

    def add(self, obj):
        self.storage.append(obj)

class TestGuestService(unittest.TestCase):
    def setUp(self):
        self.service = GuestService()
        self.repo = FakeRepo()
        self.valid_user_id = "123e4567-e89b-12d3-a456-426614174000"
        self.valid_data = {"bio": "This is a sample bio"}

    def test_register_guest_success(self):
        guest = self.service.register_as_guest(self.valid_user_id, self.valid_data, self.repo)
        self.assertEqual(guest.bio, self.valid_data["bio"])
        self.assertEqual(len(self.repo.storage), 1)

    def test_register_guest_missing_user_id(self):
        with self.assertRaises(ValueError) as ctx:
            self.service.register_as_guest(None, self.valid_data, self.repo)
        self.assertIn("user_id is required", str(ctx.exception))

    def test_register_guest_invalid_bio_type(self):
        invalid_data = {"bio": 1234}
        with self.assertRaises(ValueError) as ctx:
            self.service.register_as_guest(self.valid_user_id, invalid_data, self.repo)
        self.assertIn("bio is required and must be a string", str(ctx.exception))

    def test_register_guest_long_bio(self):
        invalid_data = {"bio": "x" * 101}
        with self.assertRaises(ValueError) as ctx:
            self.service.register_as_guest(self.valid_user_id, invalid_data, self.repo)
        self.assertIn("bio is required and must be a string with max 100 characters", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
