from app.models.amenity import Amenity

class Amenity_Service:
    def create_amenity(self, amenity_data, repo):
        new_amenity = Amenity(**amenity_data)
        repo.add(new_amenity)
        return new_amenity

    def get_amenity_info(self, amenity_id, repo):
        return repo.get(amenity_id)

    def get_all_amenities(self, repo):
        return repo.get_all()
