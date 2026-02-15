from app.models.base_model import BaseModel
from app.enums.place_amenity_status import PlaceAmenityStatus
from app.db import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    _amenity_name = db.Column("amenity_name", db.String(100), nullable=False)
    _description = db.Column("description", db.Text, nullable=True)
    _status = db.Column("status", db.String(50), nullable=True)
    _icon = db.Column("icon", db.String(50), nullable=True)

    def __init__(self, amenity_name, description, status, icon=None):
        super().__init__()
        self.amenity_name = amenity_name
        self.description = description
        self.status = status
        self.icon = icon

    @property
    def amenity_name(self):
        return self._amenity_name

    @amenity_name.setter
    def amenity_name(self, value):
        if not isinstance(value, str):
            raise ValueError("amenity_name must be a string")
        if not value or len(value) > 100:
            raise ValueError("amenity_name is required and must be <= 50 chars")
        self._amenity_name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value is None:
            self._description = None
            return
            
        if not isinstance(value, str):
            raise ValueError("description must be a string")
        if len(value) > 255:
             raise ValueError("description must be <= 255 chars")
        self._description = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, PlaceAmenityStatus):
            self._status = value.value
        else:
            try:
                self._status = PlaceAmenityStatus(value).value
            except Exception:
                raise ValueError("invalid amenity status")

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    def to_dict(self):
        return {
            "id": self.id,
            "amenity_name": self.amenity_name,
            "description": self.description,
            "icon": self.icon,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }