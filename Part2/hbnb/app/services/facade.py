from app.persistence.repository import InMemoryRepository
from app.services.user_service import UserServices
from app.services.place_service import PlaceService

class HBnBFacade:
    def __init__(self):

        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        self.user_service = UserServices()
        self.place_service = PlaceService()

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