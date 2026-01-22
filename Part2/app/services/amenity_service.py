# app/services/amenity_service.py
from app.models.amenity import Amenity
from app.enums.place_amenity_status import PlaceAmenityStatus


class AmenityService:

    def create_amenity(self, amenity_data: dict, amenity_repo):
        amenity_name = amenity_data.get("amenity_name")
        description = amenity_data.get("description")
        status = amenity_data.get("status")

        amenity = Amenity(
            amenity_name=amenity_name,
            description=description,
            status=status,
        )

        amenity_repo.add(amenity)
        return amenity

    def get_amenity_info(self, amenity_id: str, amenity_repo) -> dict:
        if not isinstance(amenity_id, str):
            raise ValueError("amenity_id must be a string")

        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if hasattr(amenity, "to_dict"):
            return amenity.to_dict()

        return {
            "id": amenity.id,
            "amenity_name": amenity.amenity_name,
            "description": amenity.description,
            "status": amenity.status.value if hasattr(amenity.status, "value") else amenity.status,
        }

    def update_amenity(self, amenity_id: str, amenity_data: dict, amenity_repo) -> bool:
        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if "amenity_name" in amenity_data:
            amenity.amenity_name = amenity_data["amenity_name"]

        if "description" in amenity_data:
            amenity.description = amenity_data["description"]

        if "status" in amenity_data:
            amenity.status = amenity_data["status"]

        amenity.save()

        return True
    
    def get_all_amenities(self, amenity_repo):
        amenities = amenity_repo.get_all()
        if not amenities:
            return []
        return amenities

    @staticmethod
    def delete_amenity(amenity_id: str, amenity_repo) -> bool:
        if not isinstance(amenity_id, str):
            raise ValueError("amenity_id must be a string")

        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        return amenity_repo.delete(amenity_id)
