from app.models.place import Place
from app.enums import place_status

class Place_Service():

    def create_place(self, place_data, repo, user_repo):

        owner = user_repo.get(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")

        title = place_data.get('title')
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("Title is required and must be a string with max 100 characters")

        price = place_data.get('price')
        if price is None or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")

        status = place_data.get('status')
        if not isinstance(status, place_status):
            raise ValueError("Invalid place status")
        
        latitude = place_data.get('latitude')
        if latitude is None or not isinstance(latitude, (int, float)) or not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude must be between -90 and 90")

        longitude = place_data.get('longitude')
        if longitude is None or not isinstance(longitude, (int, float)) or not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude must be between -180 and 180")

        description = place_data.get('description')
        if description and (not isinstance(description, str) or len(description) > 500):
            raise ValueError("Description must be a string with max 500 characters")

        place = Place(**place_data)
        repo.add(place)
        return place
