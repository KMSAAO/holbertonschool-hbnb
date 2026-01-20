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


    @property
    def rating(self):
        return self._rating
    

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("rating must be a integer")
        
        if value <= 0 or value >= 6:
            raise ValueError("rating must be between 1 to 5")
        
        self._rating = value


    
    @property
    def comment(self):
        return self._comment
    

    @comment.setter
    def comment(self, value):
        if not isinstance(value, str):
            raise ValueError("comment must be a string")
        
        if len(value) >= 250:
            raise ValueError("comment must be 250 or less")
        
        self._comment = value