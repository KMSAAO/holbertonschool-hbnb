from app.models.user import User
import re, hashlib, datetime

class UserServices():


    def register_users(self, user_data: dict, repo):

        existing_user = repo.get_by_attribute('email', user_data.get('email'))
        if existing_user:
            raise ValueError("Email already registered")

       
        first_name = user_data.get('first_name')
        if not first_name or not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("First name is required and must be a string with max 50 characters")

       
        last_name = user_data.get('last_name')
        if not last_name or not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("Last name is required and must be a string with max 50 characters")

        
        email = user_data.get('email')
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

        
        password = user_data.get('password')
        if not password or not isinstance(password, str) or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        
        is_admin = user_data.get('is_admin', False)
        is_active = user_data.get('is_active', True)

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be boolean")
        if not isinstance(is_active, bool):
            raise ValueError("is_active must be boolean")

        
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_admin=is_admin,
            is_active=is_active,
        )

        repo.add(user)
        return user
    
    def login(self, email, password, repo):
        if not email or not isinstance(email, str) or '@' not in email:
            raise ValueError("Valid email is required")

        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")


        user = repo.get_by_attribute('email', email)
        if not user:
            raise ValueError("Incorrect email or password")


        if not user.check_password(password):
            raise ValueError("Incorrect email or password")

        if user.is_active != True:
            raise ValueError("User is not active")

        return True

    def get_user_info(self, user_id, repo):
            
        if not isinstance(user_id, str):
            raise ValueError("User ID must be a string")

        user = repo.get(user_id)
        if not user:
            raise ValueError("User not found")


        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()}

    def update_user(self, user_id: str, user_data: dict, repo):

        if not isinstance(user_id, str):
            raise ValueError("User ID must be a string")

        user = repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        if "first_name" in user_data:
            if not isinstance(user_data["first_name"], str) or len(user_data["first_name"]) > 50:
                raise ValueError("Invalid first name")
            user.first_name = user_data["first_name"]

        if "last_name" in user_data:
            if not isinstance(user_data["last_name"], str) or len(user_data["last_name"]) > 50:
                raise ValueError("Invalid last name")
            user.last_name = user_data["last_name"]

        if "email" in user_data:
            if not isinstance(user_data["email"], str):
                raise ValueError("Invalid email")
            user.email = user_data["email"]

        if "password" in user_data:
            if not isinstance(user_data["password"], str) or len(user_data["password"]) < 6:
                raise ValueError("Password must be at least 6 characters")
            user.password = (user_data["password"])

        if "is_admin" in user_data:
            if not isinstance(user_data["is_admin"], bool):
                raise ValueError("is_admin must be boolean")
            user.is_admin = user_data["is_admin"]

        if "is_active" in user_data:
            if not isinstance(user_data["is_active"], bool):
                raise ValueError("is_active must be boolean")
            user.is_active = user_data["is_active"]

        return True
    
    @staticmethod
    def delete_user(user_id: str, user_repo, place_repo):

        if not isinstance(user_id, str):
            raise ValueError("User ID must be a string")

        user = user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        places = place_repo.get_all()
        for place in places:
            if hasattr(place, "user") and place.user.id == user_id:
                raise ValueError("Cannot delete user with existing places")

        return user_repo.delete(user_id)
    
    def get_all_users(self, repo):
        users = repo.get_all()
        return users