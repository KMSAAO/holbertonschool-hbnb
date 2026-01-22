import re
import hashlib

import bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):

    def __init__(self, first_name, last_name, email, password, is_admin=False, is_active=True):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("First name is required and must be a string with max 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Last name is required and must be a string with max 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email is required and must be a string")

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format")

        self._email = value

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

        self.__password = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be boolean")
        self._is_admin = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_active must be boolean")
        self._is_active = value

    def to_dict(self):
        return {
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email,
        "is_admin": self.is_admin,
        "is_active": self.is_active,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat()
        }