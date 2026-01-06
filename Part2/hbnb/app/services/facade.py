from app.persistence.repository import InMemoryRepository
from app.services.user_service import User_Service
from app.services.place_service import Place_Service
from app.services.amenity_service import Amenity_Service
from app.services.review_service import Review_Service

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

        self.user_service = User_Service()
        self.place_service = Place_Service()
        self.amenity_service = Amenity_Service()
        self.review_service = Review_Service()


    def create_user(self, user_data):
        return self.user_service.register_users(user_data, self.user_repo)

    def get_user(self, user_id):
        return self.user_service.get_user_info(user_id, self.user_repo)

    def get_all_users(self):
        return self.user_service.get_all_users(self.user_repo)


    def create_place(self, place_data):
        return self.place_service.create_place(place_data, self.place_repo, self.user_repo)

    def get_place(self, place_id):
        return self.place_service.get_place_info(place_id, self.place_repo)

    def get_all_places(self):
        return self.place_service.get_all_places(self.place_repo)

    def update_place(self, place_id, place_data):
        return self.place_service.update_place(place_id, place_data, self.place_repo)


    def create_amenity(self, amenity_data):
        return self.amenity_service.create_amenity(amenity_data, self.amenity_repo)

    def get_amenity(self, amenity_id):
        return self.amenity_service.get_amenity_info(amenity_id, self.amenity_repo)

    def get_all_amenities(self):
        return self.amenity_service.get_all_amenities(self.amenity_repo)


    def create_review(self, review_data):
        return self.review_service.create_review(review_data, self.review_repo, self.user_repo, self.place_repo)

    def get_review(self, review_id):
        return self.review_service.get_review_info(review_id, self.review_repo)

    def get_all_reviews(self):
        return self.review_service.get_all_reviews(self.review_repo)

facade = HBnBFacade()
