from app.persistence.repository import InMemoryRepository
from app.services.user_service import UserServices
from app.services.place_service import PlaceService

class HBnBFacade:
    def __init__(self):
        # Repositories
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        # Services
        self.user_service = UserServices()
        self.place_service = PlaceService()
        # بعدين تقدر تضيف ReviewService, AmenityService لو سويتها

    # ============ User Facade ============

    def register_user(self, user_data: dict) -> str:

        return self.user_service.register_users(user_data, self.user_repo)

    def login_user(self, email: str, password: str) -> bool:
        """يحاول تسجيل دخول، يرجع True أو يرمي ValueError"""
        return self.user_service.login(email, password, self.user_repo)

    def get_user(self, user_id: str) -> dict:
        """يرجع بيانات اليوزر كـ dict"""
        return self.user_service.get_user_info(user_id, self.user_repo)

    def delete_user(self, user_id: str) -> bool:
        """يحذف اليوزر لو ما عنده Places"""
        return self.user_service.delete_user(user_id, self.user_repo, self.place_repo)