from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.guest import Guest

class Review(BaseModel):

    def __init__(self, place: Place, rating, comment):

        super().__init__()

        self.place_id = place.id
        self.user_id = place.user.id
        self.place = place
        self.rating = rating
        self.comment = comment

    @classmethod
    def from_place_id(cls, place_id: str, rating: int, comment: str, place_repo):
       pass