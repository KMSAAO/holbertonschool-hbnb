# run_register.py
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place

from app.services.user_service import UserServices
from app.services.place_service import PlaceService
from app.services.facade import HBnBFacade

from app.enums.place_status import PlaceStatus

if __name__ == "__main__":
    facade = HBnBFacade()


    user: User = facade.register_user({
        "first_name": "Nawaf",
        "last_name": "Alzahrani",
        "email": "nawaf@example.com",
        "password": "AaZz123456",
        "is_admin": True,
        "is_active": True
    })

    print("✅ User ID:", user.id)
    user_info = facade.get_user(user.id)
    print("👤 User info:", user_info)

    user = facade.login_user(user.email, user.password)
    print("Success", user)