from app.models.user import User
import re, hashlib, datetime

class UserServices():


    def register_users(self, user_data: dict, repo):

        first_name = user_data.get("first_name")
        last_name  = user_data.get("last_name")
        email      = user_data.get("email")
        password   = user_data.get("password")
        is_admin   = user_data.get("is_admin", False)
        is_active  = user_data.get("is_active", True)

        if repo.get_by_attribute('email',email):
            raise ValueError("email is already register")

        
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


        if not user.verify_password(password):
            raise ValueError("Incorrect email or password")

        if user.is_active != True:
            raise ValueError("User is not active")

        return True

    def get_user_info(self, user_id, repo):
        user = repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user.to_dict()


    def update_user(self, user_id: str, user_data: dict, repo):

        user = repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        if "first_name" in user_data:
            user.first_name = user_data["first_name"]

        if "last_name" in user_data:
            user.last_name = user_data["last_name"]

        if "email" in user_data:
            user.email = user_data["email"]

        if "password" in user_data:
            user.password = user_data["password"]

        if "is_admin" in user_data:
            user.is_admin = user_data["is_admin"]

        if "is_active" in user_data:
            user.is_active = user_data["is_active"]

        return True

    
    @staticmethod
    def delete_user(user_id: str, user_repo, place_repo):

        if not isinstance(user_id, str):
            raise ValueError("User ID must be a string")

        user = user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        for place in place_repo.get_all():
            if place.user.id == user_id:
                raise ValueError("User owns places and cannot be deleted")
            
        return user_repo.delete(user_id)
    
    def get_all_users(self, repo):
        users = repo.get_all()
        return users
    

    def get_by_attribute(self, attr_name, value, repo):
        if not value:
            raise ValueError("You must enter the value")

        if not attr_name:
            raise ValueError("You must Enter the email")
        
        if not isinstance(attr_name, str):
            raise ValueError("attr_name is not correct")
        
        if not isinstance(value, str):
            raise ValueError("The value is not correct")
        
        user = repo.get_by_attribute(attr_name, value)
        return user