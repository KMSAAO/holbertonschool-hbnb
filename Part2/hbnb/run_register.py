# run_register.py

from app.services.user_service import UserServices
from app.models.user import User
from app.persistence.repository import InMemoryRepository

if __name__ == "__main__":
    repo = InMemoryRepository()
    UserService = UserServices()

    user = UserService.register_users({
        "first_name": "Nawaf",
        "last_name": "Alzahrani",
        "email": "nawaf@example.com",
        "password": "AaZz123456",
        "is_admin": True,
        "is_active": True
    }, repo)


    print("✅ User added:")
    print(user)

    # محاولة تسجيل دخول ناجحة
    is_logged_in = UserService.login("nawaf@example.com", "AaZz123456", repo)
    print("✅ Login successful:", is_logged_in)

    user_info = UserService.get_user_info(user, repo)
    print(user_info)

    UserService.update_user(
    user,
    {
        "first_name": "Saleh",
        "is_active": False
    },
    repo
)
    print('\n')
    user_info = UserService.get_user_info(user, repo)
    print(user_info)

    success = UserService.delete_user(user, repo)
    print("Deleted:", success)

    print(user_info)