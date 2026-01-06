from app.models.place import Place

class Place_Service():
    def create_place(self, place_data, repo, user_repo):
        owner = user_repo.get(place_data.get('owner_id'))
        if not owner:
            raise ValueError("Owner not found")
            
        if place_data.get('price', 0) < 0:
            raise ValueError("Price cannot be negative")

        place = Place(**place_data)
        repo.add(place)
        return place

    def get_place_info(self, place_id, repo):
        return repo.get(place_id)

    def update_place(self, place_id, update_data, repo):
        place = repo.get(place_id)
        if not place:
            return None
            
        forbidden_keys = ['id', 'created_at', 'updated_at', 'owner_id']
        for key, value in update_data.items():
            if key not in forbidden_keys and hasattr(place, key):
                setattr(place, key, value)
        
        place.last_updated()
        return place

    def get_all_places(self, repo):
        return repo.get_all()
