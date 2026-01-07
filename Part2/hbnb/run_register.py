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


    user = facade.register_user({
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

    IsLogged = facade.login_user(user.email, "AaZz123456")
    print("Success", user)

    updated = facade.update_user(user.id, {
    "first_name": "Saleh",
    "is_active": False
    })
    print(updated)

    user_info = facade.get_user(user.id)
    print("👤 User info:", user_info)

    delete_user = facade.delete_user(user.id)

