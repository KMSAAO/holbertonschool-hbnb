from models.base_model import BaseModel

class Amenity(BaseModel):

    def __init__(self,amenity_name, description, status):
        
        super().__init__()

        self.amenity_name = amenity_name
        self.description = description
        self.status = status