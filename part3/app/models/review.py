from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.guest import Guest
from app.sqlalchemy import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    _place_id = db.Column("place_id", db.String(36), db.ForeignKey('places.id'), nullable=False)
    _user_id = db.Column("user_id", db.String(36), db.ForeignKey('users.id'), nullable=False)
    _rating = db.Column("rating", db.Integer, nullable=False)
    _comment = db.Column("comment", db.Text, nullable=True)
    

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
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        self._rating = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("comment must be a string")
        if value and len(value) > 250:
            raise ValueError("comment must be 250 characters or less")
        self._comment = value

    
    def to_dict(self):
        return {
        "id": self.id,
        "place_id": self.place_id,
        "rating": self.rating,
        "comment": self.comment,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
        }
