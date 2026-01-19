from app.models.base_model import BaseModel
import hashlib

class User(BaseModel):

    def __init__(self, first_name, last_name, email, password, is_admin=False, is_active=True):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = hashlib.sha256(password.encode()).hexdigest()
        self.is_admin = is_admin
        self.is_active = is_active

    @property
    def password(self):
       raise AttributeError("Password is write-only")
    
    @password.setter
    def password(self, value):
        self.__password = hashlib.sha256(value.encode()).hexdigest()

    def check_password(self, plain_password):
        return self.__password == hashlib.sha256(plain_password.encode()).hexdigest()
