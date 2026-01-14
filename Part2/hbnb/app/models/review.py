from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):

    def __init__(self, place: Place, rating, comment):

        super().__init__()

        self.place_id = place.id
        self.place = place
        self.rating = rating
        self.comment = comment

    @classmethod
    def from_place_id(cls, place_id: str, rating: int, comment: str, place_repo):
       pass