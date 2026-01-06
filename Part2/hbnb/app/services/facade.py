from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        # Initializing Repositories
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()