from app.models.base_model import BaseModel
import hashlib
import re

class User(BaseModel):

    def __init__(self, first_name, last_name, email, password, is_admin=False, is_active=True):

        super().__init__()

        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = password
        self.is_admin = is_admin
        self.is_active = is_active


    @property
    def first_name(self):
        return self._first_name
    
    @setattr
    def first_name(self, value):
        if not value or not isinstance(self.first_name, str) or len(self.first_name) > 50:
            raise ValueError("First name is required and must be a string with max 50 characters")
        else:
            self.first_name = value

    @property
    def last_name(self):
        return self._last_name
    
    @setattr
    def last_name(self, value):
        if not value or not isinstance(self.last_name, str) or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be a string with max 50 characters")
        else:
            self._last_name = value

    @property
    def email(self):
        return self._email
    
    @setattr
    def email(self, value):
        if not value or not isinstance(self.email, str):
            raise ValueError("Email is required and must be a string")

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")
        else:
            self._email = value

    @property
    def password(self):
       raise AttributeError("Password is write-only")
    
    @password.setter
    def password(self, value):
        if not value or not isinstance(value, str) or len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        else:
            self.__password = hashlib.sha256(value.encode()).hexdigest()

    def check_password(self, plain_password):
        return self.__password == hashlib.sha256(plain_password.encode()).hexdigest()
    

    @property
    def is_admin(self):
        return self._is_admin
    
    @setattr
    def is_admin(self, value):
        if not value or not isinstance(is_admin, bool):
            raise ValueError("is_admin must be boolean")
        else:
            self._is_admin = value

    @property
    def is_active(self):
        return self._is_active
    
    @setattr
    def is_active(self, value):
        if not value or not isinstance(is_active, bool):
            raise ValueError("is_active must be boolean")
        else:
            self._is_active = value