from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):

    def __init__(self, place: Place, user: User, rating, comment):

        super().__init__()
        self.place = place
        self.user = user
        self.rating = rating
        self.comment = comment