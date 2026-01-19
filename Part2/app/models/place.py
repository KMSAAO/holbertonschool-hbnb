from app.models.base_model import BaseModel
from app.models.user import User
from app.enums import place_status

class Place(BaseModel):

    def __init__(self, user: User, title, description, price, status: place_status, latitude, longitude):

        super().__init__()
        self.user_id = user.id
        self.user = user
        self.title = title
        self.description = description
        self.price = price
        self.status = status
        self.latitude = latitude
        self.longitude = longitude