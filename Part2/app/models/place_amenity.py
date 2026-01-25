from app.models.base_model import BaseModel
from app.enums import place_amenity_status


class PlaceAmenity(BaseModel):
    def __init__(self, place_id: str, amenity_id: str, status: place_amenity_status):
        super().__init__()
        self.place_id = place_id
        self.amenity_id = amenity_id
        self.status = status

    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, str):
            raise ValueError("place_id must be a string")
        self._place_id = value

    @property
    def amenity_id(self):
        return self._amenity_id

    @amenity_id.setter
    def amenity_id(self, value):
        if not isinstance(value, str):
            raise ValueError("amenity_id must be a string")
        self._amenity_id = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, place_amenity_status):
            raise ValueError("status must be an instance of place_amenity_status Enum")
        self._status = value

    def to_dict(self):
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
