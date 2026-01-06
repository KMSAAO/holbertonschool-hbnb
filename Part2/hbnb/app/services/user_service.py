from app.models.user import User
import re

class UserServices():


    def register_users(self, user_data, repo):

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
            raise ValueError("Password is required and must be at least 6 characters")


        is_admin = user_data.get('is_admin', False)
        is_active = user_data.get('is_active', True)
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be boolean")
        if not isinstance(is_active, bool):
            raise ValueError("is_active must be boolean")


        user = User(**user_data)
        repo.add(user)
        return user.id