from app.models.place import Place
from app.enums.place_status import PlaceStatus
from datetime import datetime

class PlaceService():

    def create_place(self, place_data: dict, repo, user_repo):
        owner_id = place_data.get('owner_id')
        owner = user_repo.get(owner_id)
        title = place_data.get('title')
        description = place_data.get('description')
        price = place_data.get('price')
        status = place_data.get('status')
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')


        place = Place(
            user=owner,
            title=title,
            description=description,
            price=price,
            status=status,
            latitude=latitude,
            longitude=longitude
        )
        repo.add(place)

        place.owner_id = owner.id 

        return place

    def get_place_info(self, place_id: str, place_repo) -> dict:
        if not isinstance(place_id, str):
            raise ValueError("Place ID must be a string")

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "status": place.status.value,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.user.id,
            "created_at": place.created_at,
            "updated_at": place.updated_at
        }
    
    def update_place(self, place_id: str, place_data: dict, place_repo) -> bool:

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        if "title" in place_data:
            place.title = place_data["title"]

        if "description" in place_data:
            place.description = place_data["description"]

        if "price" in place_data:
            place.price = place_data["price"]

        if "latitude" in place_data:
            place.latitude = place_data["latitude"]

        if "longitude" in place_data:
            place.longitude = place_data["longitude"]

        if "status" in place_data:
            place.status = place_data["status"]

        return True
    
    def get_all_places(self, place_repo):
        return place_repo.get_all()

    @staticmethod
    def delete_place(place_id: str, place_repo) -> bool:
        if not isinstance(place_id, str):
            raise ValueError("Place ID must be a string")

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        return place_repo.delete(place_id)
