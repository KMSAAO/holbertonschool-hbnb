from app.models.place_amenity import PlaceAmenity
from app.enums.place_amenity_status import PlaceAmenityStatus


class PlaceAmenityService:

    def add_amenity_to_place(self, place_id: str, amenity_id: str, repo):
        # نحتفظ بالتحقق هنا لأنه ارتباط خارجي
        if not place_id or not isinstance(place_id, str):
            raise ValueError("place_id is required and must be a string")
        
        if not amenity_id or not isinstance(amenity_id, str):
            raise ValueError("amenity_id is required and must be a string")
        
        new_place_amenity = PlaceAmenity(
            place_id=place_id,
            amenity_id=amenity_id,
            status=PlaceAmenityStatus.ACTIVE
        )
        repo.add(new_place_amenity)
        return new_place_amenity

    def remove_amenity_from_place(self, place_amenity_id: str, repo):
        place_amenity = repo.get(place_amenity_id)
        if not place_amenity:
            raise ValueError("PlaceAmenity not found")
        
        return repo.delete(place_amenity_id)

    def get_place_amenity_info(self, place_amenity_id: str, repo) -> dict:
        place_amenity = repo.get(place_amenity_id)
        if not place_amenity:
            raise ValueError("PlaceAmenity not found")
        
        return {
            "id": place_amenity.id,
            "place_id": place_amenity.place_id,
            "amenity_id": place_amenity.amenity_id,
            "status": place_amenity.status.value
        }

    def update_place_amenity_status(self, place_amenity_id: str, status: str, repo) -> bool:
        place_amenity = repo.get(place_amenity_id)
        if not place_amenity:
            raise ValueError("PlaceAmenity not found")
        
        try:
            new_status = status if isinstance(status, PlaceAmenityStatus) else PlaceAmenityStatus(status)
        except Exception:
            raise ValueError("Invalid status value")

        place_amenity.status = new_status
        return repo.update(place_amenity)


    def get_all_amenities_for_place(self,repo):
        all_place_amenities = repo.get_all()

        if not all_place_amenities:
            return None
        return all_place_amenities