from app.models.base_model import BaseModel
from app.enums.place_amenity_status import PlaceAmenityStatus

class Amenity(BaseModel):

    def __init__(self, amenity_name, description, status):
        
        super().__init__()

        self.amenity_name = amenity_name
        self.description = description
        self.status = status


    @property
    def amenity_name(self):
        return self._amenity_name
    

    @amenity_name.setter
    def amenity_name(self, value):
        if not isinstance(value, str):
            raise ValueError("amenity_name must be string")
        if not value or len(value) > 50:
            raise ValueError("amenity_name is required and must be <= 50 chars")

        self._amenity_name = value


    @property
    def description(self):
        return self._description
    

    @description.setter
    def description(self, value):
         if not isinstance(value, str):
            raise ValueError("description must be string")
         if not value or len(value) > 100:
            raise ValueError("description must be <= 100 chars")
         self._description = value
         
    
    @property
    def status(self):
        return self._status
    

    @status.setter
    def status(self, value):
        if isinstance(value, PlaceAmenityStatus):
            self._status = value
        else:
            try:
                self._status = PlaceAmenityStatus(value)
            except Exception:
                raise ValueError("invalid amenity status")
            
    def to_dict(self):
        return {
            "id": self.id,
            "amenity_name": self.amenity_name,
            "description": self.description,
            "status": self.status.value if hasattr(self.status, "value") else self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }