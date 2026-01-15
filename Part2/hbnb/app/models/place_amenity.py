from app.models.base_model import BaseModel
from app.enums import place_amenity_status


class PlaceAmenity(BaseModel):
    
    def __init__(self, place_id, amenity_id, status: place_amenity_status):
        super().__init__()

        self.place_id = place_id
        self.amenity_id = amenity_id
        self.status = status