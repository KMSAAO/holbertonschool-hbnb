import unittest

from app.services.amenity_service import AmenityService
from app.persistence.repository import InMemoryRepository
from app.enums.place_amenity_status import PlaceAmenityStatus


class TestAmenityService(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryRepository()
        self.service = AmenityService()

    def test_create_amenity_success(self):
        data = {
            "amenity_name": "Pool",
            "description": "Nice pool",
            "status": "ACTIVE"
        }

        amenity = self.service.create_amenity(data, self.repo)

        self.assertIsNotNone(amenity.id)
        self.assertEqual(amenity.amenity_name, "Pool")
        self.assertEqual(amenity.description, "Nice pool")
        # enum يتحول من سترنق
        self.assertIsInstance(amenity.status, PlaceAmenityStatus)
        self.assertEqual(amenity.status, PlaceAmenityStatus.ACTIVE)

    def test_create_amenity_invalid_name(self):
        data = {
            "amenity_name": "",
            "description": "Bad",
            "status": "ACTIVE"
        }

        with self.assertRaises(ValueError):
            self.service.create_amenity(data, self.repo)

    def test_get_amenity_info_success(self):
        # نضيف يدوي في الريبو
        data = {
            "amenity_name": "Parking",
            "description": "Free parking",
            "status": PlaceAmenityStatus.ACTIVE
        }
        amenity = self.service.create_amenity(data, self.repo)

        info = self.service.get_amenity_info(amenity.id, self.repo)

        self.assertEqual(info["id"], amenity.id)
        self.assertEqual(info["amenity_name"], "Parking")
        self.assertEqual(info["status"], "ACTIVE")

    def test_update_amenity_success(self):
        data = {
            "amenity_name": "Gym",
            "description": "Basic gym",
            "status": "ACTIVE"
        }
        amenity = self.service.create_amenity(data, self.repo)

        update_data = {
            "amenity_name": "Gym Updated",
            "description": "24/7 gym",
            "status": "INACTIVE"
        }

        result = self.service.update_amenity(amenity.id, update_data, self.repo)
        self.assertTrue(result)

        updated = self.repo.get(amenity.id)
        self.assertEqual(updated.amenity_name, "Gym Updated")
        self.assertEqual(updated.description, "24/7 gym")
        self.assertEqual(updated.status, PlaceAmenityStatus.INACTIVE)

    def test_delete_amenity_success(self):
        data = {
            "amenity_name": "Spa",
            "description": "Relax",
            "status": "ACTIVE"
        }
        amenity = self.service.create_amenity(data, self.repo)

        deleted = self.service.delete_amenity(amenity.id, self.repo)
        self.assertTrue(deleted)
        self.assertIsNone(self.repo.get(amenity.id))


if __name__ == "__main__":
    unittest.main()