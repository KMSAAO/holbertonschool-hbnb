from app.models.base_model import BaseModel
from app.models.user import User
from app.enums import place_status
from app.enums.place_status import PlaceStatus
from app.sqlalchemy import db

class Place(BaseModel):

    __tablename__ = 'places'

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    def __init__(self, user_id, title, description, price, status: place_status, latitude, longitude):

        super().__init__()
        self.user_id = user_id
        self.title = title
        self.description = description
        self.price = price
        self.status = status
        self.latitude = latitude
        self.longitude = longitude


    @property
    def user_id(self):
        return self._user_id
    
    
    @user_id.setter
    def user_id(self, value):
        if not value:
            raise ValueError("Owner not found")
        else:
            self._user_id = value


    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError("Title is required and must be a string with max 100 characters")
        else:
            self._title = value


    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if value and (not isinstance(value, str) or len(value) > 500):
            raise ValueError("Description must be a string with max 500 characters")
        else:
            self._description = value

    @property
    def price(self):
        return self._price
    

    @price.setter
    def price(self, value):
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        else:
            self._price = value


    @property
    def status(self):
        return self._status
    

    @status.setter
    def status(self, value):
        if isinstance(value, PlaceStatus):
            self._status = value
        else:
            try:
                self._status = PlaceStatus(value)
            except Exception:
                raise ValueError("Invalid place status")
            

    @property
    def latitude(self):
        return self._latitude
    
    
    @latitude.setter
    def latitude(self, value):
        if value is None or not isinstance(value, (int, float)) or not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        else:
            self._latitude = value


    @property
    def longitude(self):
        return self._longitude
    

    @longitude.setter
    def longitude(self, value):
        if value is None or not isinstance(value, (int, float)) or not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        else:
            self._longitude = value