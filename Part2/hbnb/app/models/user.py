from app.models.base_model import BaseModel
import hashlib, re

class User(BaseModel):

    def __init__(self, first_name, last_name, email, password, is_admin = False, is_active = True):

        super().__init__()
        
        if not first_name or not isinstance(first_name, str):
            raise ValueError("First name is required and must be a string")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or fewer")

        if not last_name or not isinstance(last_name, str):
            raise ValueError("Last name is required and must be a string")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or fewer")

        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")
        
        if not isinstance(is_active, bool):
            raise ValueError("is_active must be a boolean")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = hashlib.sha256(password.encode()).hexdigest()
        self.is_admin = is_admin
        self.is_active = is_active