from app.models.place import Place
from app.enums.place_status import PlaceStatus
from datetime import datetime

class PlaceService():

    def create_place(self, place_data: dict, repo, user_db, amenity_repo):
        owner_id = place_data.get('owner_id')
        owner = user_db.get(owner_id)

        title = place_data.get('title')
        description = place_data.get('description')
        price = place_data.get('price')
        status = place_data.get('status', PlaceStatus.AVAILABLE)
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')
        location = place_data.get('location')
        amenities_data = place_data.get('amenities', [])
        
        # New fields for Phase 3
        number_of_rooms = place_data.get('number_of_rooms', 0)
        max_guests = place_data.get('max_guests', 0)
        tagline = place_data.get('tagline')
        rules = place_data.get('rules')
        details = place_data.get('details') # Expecting JSON string or list
        rooms = place_data.get('rooms', [])

        place = Place(
            user_id=owner.id,
            title=title,
            description=description,
            price=price,
            status=status,
            latitude=latitude,
            longitude=longitude,
            number_of_rooms=number_of_rooms,
            max_guests=max_guests,
            tagline=tagline,
            rules=rules,
            details=details,
            rooms=rooms,
            location=location
        )

        # Handle amenities
        if amenities_data:
            from app.models.amenity import Amenity
            from app.enums.place_amenity_status import PlaceAmenityStatus
            
            for amenity_item in amenities_data:
                # admin.js sends {icon: "...", text: "..."}
                amenity_name = amenity_item.get('text') if isinstance(amenity_item, dict) else amenity_item
                amenity_icon = amenity_item.get('icon') if isinstance(amenity_item, dict) else None
                
                if amenity_name:
                    # Check if exists
                    # Note: Attribute is _amenity_name in Amenity model
                    # get_by_attribute uses filter_by(**kwargs), so we must use the MAPPED column name.
                    existing_amenity = amenity_repo.get_by_attribute('_amenity_name', amenity_name)

                    if existing_amenity:
                        place.amenities.append(existing_amenity)
                    else:
                        new_amenity = Amenity(
                            amenity_name=amenity_name,
                            description=None,
                            status=PlaceAmenityStatus.ACTIVE, # Default status
                            icon=amenity_icon
                        )
                        amenity_repo.add(new_amenity)
                        place.amenities.append(new_amenity)

        repo.add(place)

        place.owner_id = owner.id 

        return place

    def get_place(self, place_id: str, place_repo):
        return place_repo.get(place_id)

    def get_place_info(self, place_id: str, place_repo) -> dict:
        if not isinstance(place_id, str):
            raise ValueError("Place ID must be a string")

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        if place:
            place_dict = {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner_id,
                "owner": {
                    "id": place.user.id,
                    "first_name": place.user.first_name,
                    "last_name": place.user.last_name,
                    "email": place.user.email
                } if place.user else None,
                "amenities": [amenity.to_dict() for amenity in place.amenities],
                "reviews": [
                    {
                        **review.to_dict(),
                        "user": {
                            "id": review.user.id,
                            "first_name": review.user.first_name,
                            "last_name": review.user.last_name
                        } if review.user else None
                    }
                    for review in place.reviews
                ],
                "images": [],
                "number_of_rooms": place.number_of_rooms,
                "max_guests": place.max_guests,
                "tagline": place.tagline,
                "rules": place.rules,
                "details": place.details,
                "rooms": place.rooms,
                "location": place.location
            }
            
            # Handle images if they are stored as JSON string or list
            if place.images:
                try:
                    import json
                    if isinstance(place.images, str):
                        place_dict["images"] = json.loads(place.images)
                    else:
                        place_dict["images"] = place.images
                except:
                    place_dict["images"] = []
            
            return place_dict
    
    def update_place(self, place_id: str, place_data: dict, place_repo, amenity_repo=None) -> bool:

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

        if "images" in place_data:
            place.images = place_data["images"]

        # New fields updates
        if "number_of_rooms" in place_data:
            place.number_of_rooms = place_data["number_of_rooms"]
            
        if "max_guests" in place_data:
            place.max_guests = place_data["max_guests"]
            
        if "tagline" in place_data:
            place.tagline = place_data["tagline"]
            
        if "rules" in place_data:
            place.rules = place_data["rules"]
            
        if "details" in place_data:
            place.details = place_data["details"]

        if "rooms" in place_data:
            place.rooms = place_data["rooms"]

        if "location" in place_data:
            place.location = place_data["location"]

        if "amenities" in place_data:
            if not amenity_repo:
                raise ValueError("amenity repository unavailable")

            amenity_ids = place_data["amenities"]
            if not isinstance(amenity_ids, list):
                raise ValueError("amenities must be a list of IDs")

            normalized_ids = []
            seen_ids = set()
            for raw_id in amenity_ids:
                if not isinstance(raw_id, str):
                    raise ValueError("amenities must be a list of amenity ID strings")

                amenity_id = raw_id.strip()
                if not amenity_id:
                    raise ValueError("amenities contains an empty amenity ID")

                if amenity_id in seen_ids:
                    continue

                seen_ids.add(amenity_id)
                normalized_ids.append(amenity_id)

            new_amenities = []
            for amenity_id in normalized_ids:
                amenity = amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity not found: {amenity_id}")
                new_amenities.append(amenity)

            # Atomic replace after full validation
            place.amenities = new_amenities

        return True
    
    def get_all_places(self, place_repo):
        return place_repo.get_all()

    def delete_place(self, place_id: str, place_repo) -> bool:
        if not isinstance(place_id, str):
            raise ValueError("Place ID must be a string")

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        return place_repo.delete(place_id)

    def get_places_by_user(self, user_id: str, place_repo):
        return place_repo.get_all_by_attribute('_user_id', user_id)

    def add_amenity(self, place_id: str, amenity_id: str, place_repo, amenity_repo) -> bool:
        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if amenity in place.amenities:
            raise ValueError("Amenity already added to place")

        place.amenities.append(amenity)
        # Assuming repository handles persistence on modification or explicit update/save is needed.
        # SQLAlchemy usually needs a commit. If repo.add/update does commit, we might need to call it.
        # Since we modified the relationship, often just committing the session is enough.
        # But here we don't have direct session access.
        # Let's try calling update logic if repo supports it, or assume ORM handles it.
        # Ideally, we should have a generic save/update. 
        # Re-adding the place to repo might trigger merge/commit.
        place_repo.add(place) 
        return True

    def remove_amenity(self, place_id: str, amenity_id: str, place_repo, amenity_repo) -> bool:
        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if amenity not in place.amenities:
            raise ValueError("Amenity not linked to place")

        place.amenities.remove(amenity)
        place_repo.add(place)
        return True
