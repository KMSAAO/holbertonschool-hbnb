from app.persistence.repository import InMemoryRepository
from app.services.user_service import User_Service
from app.services.place_service import Place_Service
from app.services.amenity_service import Amenity_Service

class HBnBFacade:
    def __init__(self):
        # Initializing Repositories
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        # Initializing Services
        self.user_service = User_Service()
        self.place_service = Place_Service()
        self.amenity_service = Amenity_Service()

    # --- User Methods ---
    def create_user(self, user_data):
        """Registers a new user in the system"""
        return self.user_service.register_users(user_data, self.user_repo)

    def get_user(self, user_id):
        """Retrieves user information by ID"""
        return self.user_service.get_user_info(user_id, self.user_repo)

    def get_all_users(self):
        """Returns a list of all registered users"""
        return self.user_service.get_all_users(self.user_repo)

    # --- Place Methods ---
    def create_place(self, place_data):
        """Creates a place and links it to a valid owner"""
        return self.place_service.create_place(place_data, self.place_repo, self.user_repo)

    def get_place(self, place_id):
        """Retrieves details of a specific place"""
        return self.place_service.get_place_info(place_id, self.place_repo)

    def get_all_places(self):
        """Returns all available places"""
        return self.place_service.get_all_places(self.place_repo)

    def update_place(self, place_id, place_data):
        """Updates information for an existing place"""
        return self.place_service.update_place(place_id, place_data, self.place_repo)

    # --- Amenity Methods ---
    def create_amenity(self, amenity_data):
        """Adds a new amenity to the repository"""
        return self.amenity_service.create_amenity(amenity_data, self.amenity_repo)

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by its ID"""
        return self.amenity_service.get_amenity_info(amenity_id, self.amenity_repo)

    def get_all_amenities(self):
        """Returns a list of all amenities"""
        return self.amenity_service.get_all_amenities(self.amenity_repo)

facade = HBnBFacade()
