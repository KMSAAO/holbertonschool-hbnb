from app.models.base_model import BaseModel
from app.models.user import User

class Guest(BaseModel):

    def __init__(self,user: User, user_id, bio):
        super().__init__()
        self.user_id = user_id
        self.user = user
        self.bio = bio