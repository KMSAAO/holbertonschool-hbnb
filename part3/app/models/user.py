import re
from app.bcrypt import bcrypt
from app.db import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship


class User(BaseModel):

    __tablename__= 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    reviews = relationship("Review", backref="user", cascade="all, delete-orphan", lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False, is_active=True):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_value = password
        self.is_admin = is_admin
        self.is_active = is_active

    @property
    def first_name_value(self):
        return self.first_name

    @first_name_value.setter
    def first_name_value(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("First name is required and must be a string with max 50 characters")
        self.first_name = value

    @property
    def last_name_value(self):
        return self.last_name

    @last_name_value.setter
    def last_name_value(self, value):
        if not value or not isinstance(value, str) or len(value) > 50:
            raise ValueError("Last name is required and must be a string with max 50 characters")
        self.last_name = value

    @property
    def email_value(self):
        return self.email

    @email_value.setter
    def email_value(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email is required and must be a string")

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, value):
            raise ValueError("Invalid email format")

        self.email = value

    @property
    def password_value(self):
        return self.password


    @password_value.setter
    def password_value(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @property
    def is_admin_value(self):
        return self.is_admin

    @is_admin_value.setter
    def is_admin_value(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be boolean")
        self.is_admin = value

    @property
    def is_active_value(self):
        return self.is_active

    @is_active_value.setter
    def is_active_value(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_active must be boolean")
        self.is_active = value

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