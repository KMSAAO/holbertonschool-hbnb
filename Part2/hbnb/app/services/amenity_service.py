# app/services/amenity_service.py
from app.models.amenity import Amenity
from app.enums.place_amenity_status import PlaceAmenityStatus


class AmenityService:

    def create_amenity(self, amenity_data: dict, amenity_repo):
        amenity_name = amenity_data.get("amenity_name")
        if not amenity_name or not isinstance(amenity_name, str) or len(amenity_name) > 100:
            raise ValueError("amenity_name is required and must be <= 100 chars")

        description = amenity_data.get("description", "")
        if not isinstance(description, str) or len(description) > 500:
            raise ValueError("description must be <= 500 chars")

        raw_status = amenity_data.get("status", PlaceAmenityStatus.ACTIVE)
        if isinstance(raw_status, PlaceAmenityStatus):
            status = raw_status
        else:
            try:
                status = PlaceAmenityStatus(raw_status)
            except Exception:
                raise ValueError("invalid amenity status")

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
        if not isinstance(amenity_id, str):
            raise ValueError("amenity_id must be a string")

        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if "amenity_name" in amenity_data:
            amenity_name = amenity_data["amenity_name"]
            if not amenity_name or not isinstance(amenity_name, str) or len(amenity_name) > 100:
                raise ValueError("invalid name")
            amenity.amenity_name = amenity_name

        if "description" in amenity_data:
            desc = amenity_data["description"]
            if not isinstance(desc, str) or len(desc) > 500:
                raise ValueError("invalid description")
            amenity.description = desc

        if "status" in amenity_data:
            raw_status = amenity_data["status"]
            if isinstance(raw_status, PlaceAmenityStatus):
                status = raw_status
            else:
                try:
                    status = PlaceAmenityStatus(raw_status)
                except Exception:
                    raise ValueError("invalid amenity status")
            amenity.status = status

        amenity_repo.update(amenity)

        return True

    @staticmethod
    def delete_amenity(amenity_id: str, amenity_repo) -> bool:
        if not isinstance(amenity_id, str):
            raise ValueError("amenity_id must be a string")

        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        return amenity_repo.delete(amenity_id)
