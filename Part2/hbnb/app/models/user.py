from models.base_model import BaseModel


class User(BaseModel):

    def __init__(self, first_name, last_name, email, password, is_admin = False, is_active = True):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = password
        self.is_admin = is_admin
        self.is_active = is_active