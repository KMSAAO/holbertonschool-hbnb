from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.guest import Guest

class Review(BaseModel):

    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, str):
            raise ValueError("place_id must be a string")
        self._place_id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, str):
            raise ValueError("user_id must be a string")
        self._user_id = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("rating must be an integer")
        if value <= 0 or value >= 6:
            raise ValueError("rating must be between 1 and 5")
        self._rating = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if not isinstance(value, str):
            raise ValueError("comment must be a string")
        if len(value) >= 250:
            raise ValueError("comment must be 250 characters or less")
        self._comment = value
    
    def to_dict(self):
        return {
        "id": self.id,
        "place_id": self.place_id,
        "user_id" : self.user_id,
        "rating": self.rating,
        "comment": self.comment,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
        }
