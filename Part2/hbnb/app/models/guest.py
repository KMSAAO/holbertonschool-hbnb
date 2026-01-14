from app.models.base_model import BaseModel

class Guest(BaseModel):

    def __init__(self, bio):
        super().__init__()
        self.bio = bio