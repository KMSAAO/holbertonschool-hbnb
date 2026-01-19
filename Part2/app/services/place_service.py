from app.models.place import Place
from app.enums.place_status import PlaceStatus

class PlaceService():

    def create_place(self, place_data: dict, repo, user_repo):
        owner_id = place_data.get('owner_id')
        if not owner_id or not isinstance(owner_id, str):
            raise ValueError("owner_id is required and must be a string")

        owner = user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        title = place_data.get('title')
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("Title is required and must be a string with max 100 characters")
        
        description = place_data.get('description')
        if description and (not isinstance(description, str) or len(description) > 500):
            raise ValueError("Description must be a string with max 500 characters")

        price = place_data.get('price')
        if price is None or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")

        raw_status = place_data.get('status')
        if isinstance(raw_status, PlaceStatus):
            status = raw_status
        else:
            try:
                status = PlaceStatus(raw_status)
            except Exception:
                raise ValueError("Invalid place status")

        latitude = place_data.get('latitude')
        if latitude is None or not isinstance(latitude, (int, float)) or not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90 and 90")

        longitude = place_data.get('longitude')
        if longitude is None or not isinstance(longitude, (int, float)) or not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180 and 180")


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
            "owner_id": place.user.id
        }
    
    def update_place(self, place_id: str, place_data: dict, place_repo, user_repo) -> bool:
        if not isinstance(place_id, str):
            raise ValueError("Place ID must be a string")

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        updates = {}

        if "user_id" in place_data or "owner_id" in place_data:
            owner_id = place_data.get("user_id") or place_data.get("owner_id")
            if not isinstance(owner_id, str):
                raise ValueError("user_id must be a string")
            owner = user_repo.get(owner_id)
            if not owner:
                raise ValueError("Owner not found")
            place.user = owner
            updates['user_id'] = owner_id

        if "title" in place_data:
            title = place_data["title"]
            if not title or not isinstance(title, str) or len(title) > 100:
                raise ValueError("Invalid title")
            place.title = title
            updates['title'] = title

        if "description" in place_data:
            desc = place_data["description"]
            if desc and (not isinstance(desc, str) or len(desc) > 500):
                raise ValueError("Invalid description")
            place.description = desc
            updates['description'] = desc

        if "price" in place_data:
            price = place_data["price"]
            if price is None or not isinstance(price, (int, float)) or price < 0:
                raise ValueError("Invalid price")
            place.price = price
            updates['price'] = price

        if "latitude" in place_data:
            lat = place_data["latitude"]
            if lat is None or not isinstance(lat, (int, float)) or not -90.0 <= lat <= 90.0:
                raise ValueError("Invalid latitude")
            place.latitude = lat
            updates['latitude'] = lat

        if "longitude" in place_data:
            lon = place_data["longitude"]
            if lon is None or not isinstance(lon, (int, float)) or not -180.0 <= lon <= 180.0:
                raise ValueError("Invalid longitude")
            place.longitude = lon
            updates['longitude'] = lon

        if "status" in place_data:
            raw_status = place_data["status"]
            if isinstance(raw_status, PlaceStatus):
                status = raw_status
            else:
                try:
                    status = PlaceStatus(raw_status)
                except Exception:
                    raise ValueError("Invalid place status")
            place.status = status
            updates['status'] = status

        place_repo.update(place_id, updates)
        return True

    @staticmethod
    def delete_place(place_id: str, place_repo) -> bool:
        if not isinstance(place_id, str):
            raise ValueError("Place ID must be a string")

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        return place_repo.delete(place_id)
