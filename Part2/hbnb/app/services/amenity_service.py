from app.models.amenity import Amenity

class Amenity_Service():
    def create_amenity(self, amenity_data, repo):
        
        name = amenity_data.get('amenity_name')
        desc = amenity_data.get('description')
        status = amenity_data.get('status')
        if not name:
            raise ValueError("Amenity name is required")
        
        if len(desc) > 250:
            raise ValueError("Description is too long")
        amenity = Amenity(**amenity_data)

        repo.add(amenity)

        return amenity.id

    def get_amenity_info(self, amenity_id, repo): 
        amenity = repo.get(amenity_id)

        if not amenity:
            return None
        return amenity

    def update_amenity(self, amenity_id, update_data, repo):
        amenity = repo.get(amenity_id)
        if not amenity:
            return None
        
        forbidden_keys = ['id', 'created_at', 'updated_at']

        for key, value in update_data.items():
            if key in forbidden_keys:
                continue
            
            if hasattr(amenity, key):
                setattr(amenity, key, value)

        amenity.last_updated()

        return amenity
    def delete_amenity(self, amenity_id, repo):
        success = repo.delete(amenity_id)

        return success