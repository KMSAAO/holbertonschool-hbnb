from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, place: Place, user: User, rating, text):
        super().__init__()

        self.place = place
        self.place_id = place.id
        
        self.user = user
        self.user_id = user.id
        
        self.rating = rating
        
        self.text = text

    @classmethod
    def from_place_id(cls, place_id: str, user_id: str, rating: int, text: str, place_repo, user_repo):
        place = place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found")
            
        user = user_repo.get(user_id)
        if user is None:
            raise ValueError("User not found")

        return cls(place=place, user=user, rating=rating, text=text)