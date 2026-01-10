from app.persistence.repository import InMemoryRepository
from app.services.user_service import UserServices
from app.services.place_service import PlaceService
from app.services.amenity_service import AmenityService
from app.services.review_service import ReviewService

class HBnBFacade:
    def __init__(self):

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        self.user_service = UserServices()
        self.place_service = PlaceService()
        self.review_service = ReviewService()
        self.amenity_service = AmenityService()

    """User Methods"""
    def register_user(self, user_data: dict) -> str:

        return self.user_service.register_users(user_data, self.user_repo)

    def login_user(self, email: str, password: str) -> bool:
        return self.user_service.login(email, password, self.user_repo)

    def get_user(self, user_id: str) -> dict:

        return self.user_service.get_user_info(user_id, self.user_repo)

    def update_user(self, user_id: str, user_data: dict) -> bool:
        
        return self.user_service.update_user(user_id, user_data, self.user_repo)
    
    def delete_user(self, user_id: str) -> bool:

        return self.user_service.delete_user(user_id, self.user_repo, self.place_repo)
    
    """Place Methods"""
    def create_place(self, place_data: dict):

        return self.place_service.create_place(
            place_data=place_data,
            repo=self.place_repo,
            user_repo=self.user_repo
        )

    def get_place_info(self, place_id: str) -> dict:

        return self.place_service.get_place_info(
            place_id=place_id,
            place_repo=self.place_repo
        )

    def update_place(self, place_id: str, place_data: dict) -> bool:

        return self.place_service.update_place(
            place_id=place_id,
            place_data=place_data,
            place_repo=self.place_repo,
            user_repo=self.user_repo
        )

    def delete_place(self, place_id: str) -> bool:

        return self.place_service.delete_place(
            place_id=place_id,
            place_repo=self.place_repo
        )

    """review Methods"""
    def create_review(self, review_data: dict) -> dict:
        return self.review_service.create_Review(
        review_data=review_data,
        place_repo=self.place_repo,
        review_repo=self.review_repo,
    )


    def get_review_info(self, review_id: str) -> dict:
        return self.review_service.get_review_info(
            review_id=review_id,
            review_repo=self.review_repo
        )

    def update_review(self, review_id: str, review_data: dict) -> bool:
        return self.review_service.update_review(
            review_id,
            review_data,
            self.review_repo
        )   

    def delete_review(self, review_id: str) -> bool:
        return self.review_service.delete_Review(
            review_id, self.review_repo
        )


    """Amenity Methods"""
    def create_amenity(self, amenity_data: dict):
        return self.amenity_service.create_amenity(
            amenity_data,
            self.amenity_repo
        )

    def get_amenity_info(self, amenity_id: str) -> dict:
        return self.amenity_service.get_amenity_info(
            amenity_id,
            self.amenity_repo
        )

    def update_amenity(self, amenity_id: str, amenity_data: dict) -> bool:
        return self.amenity_service.update_amenity(
            amenity_id,
            amenity_data,
            self.amenity_repo
        )

    def delete_amenity(self, amenity_id: str) -> bool:
        return self.amenity_service.delete_amenity(
            amenity_id,
            self.amenity_repo
        )