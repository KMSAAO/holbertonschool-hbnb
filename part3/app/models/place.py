import json
from app.models.base_model import BaseModel
from app.enums import place_status
from app.enums.place_status import PlaceStatus
from app.db import db
from sqlalchemy.orm import relationship

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    _user_id = db.Column("user_id", db.String(36), db.ForeignKey('users.id'), nullable=False)
    _title = db.Column("title", db.String(128), nullable=False)
    _description = db.Column("description", db.Text, nullable=True)
    _price = db.Column("price", db.Float, nullable=False)
    _status = db.Column("status", db.String(50), nullable=True)
    _latitude = db.Column("latitude", db.Float, nullable=True)
    _longitude = db.Column("longitude", db.Float, nullable=True)
    _images = db.Column("images", db.Text, nullable=True, default='[]')
    
    # New fields for Phase 3
    _number_of_rooms = db.Column("number_of_rooms", db.Integer, default=0)
    _max_guests = db.Column("max_guests", db.Integer, default=0)
    _tagline = db.Column("tagline", db.String(255), nullable=True)
    _rules = db.Column("rules", db.Text, nullable=True)
    _details = db.Column("details", db.Text, nullable=True) # JSON for about sections
    _rooms = db.Column("rooms", db.Text, nullable=True, default='[]') # JSON for room list
    _location = db.Column("location", db.String(255), nullable=True)

    user = relationship("User", backref="places")

    reviews = relationship("Review", backref="place", cascade="all, delete-orphan", lazy=True)

    amenities = relationship("Amenity", secondary=place_amenity, backref="places", lazy=True)

    def __init__(self, user_id, title, description, price, status, latitude, longitude,
                 number_of_rooms=0, max_guests=0, tagline=None, rules=None, details=None, rooms=None, location=None):
        super().__init__()
        self.owner_id = user_id
        self.title = title
        self.description = description
        self.price = price
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_rooms = number_of_rooms
        self.max_guests = max_guests
        self.tagline = tagline
        self.rules = rules
        self.details = details or '[]'
        self.rooms = rooms or []
        self.location = location
        self.amenities = []
        self.reviews = []


    @property
    def owner_id(self):
        return self._user_id

    @owner_id.setter
    def owner_id(self, value):
        if not value:
            raise ValueError("Owner not found")
        self._user_id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str) or len(value) > 100:
            raise ValueError("Title is required and must be a string with max 100 characters")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value and (not isinstance(value, str) or len(value) > 500):
            raise ValueError("Description must be a string with max 500 characters")
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, PlaceStatus):
            self._status = value.value
        else:
            try:
                self._status = PlaceStatus(value).value
            except Exception:
                raise ValueError("Invalid place status")

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if value is None or not isinstance(value, (int, float)) or not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if value is None or not isinstance(value, (int, float)) or not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    @property
    def images(self):
        if not self._images:
            return []
        try:
            return json.loads(self._images)
        except (json.JSONDecodeError, TypeError):
            return []

    @images.setter
    def images(self, value):
        if isinstance(value, list):
            self._images = json.dumps(value)
        elif isinstance(value, str):
            self._images = value
        else:
            self._images = '[]'

    @property
    def number_of_rooms(self):
        return self._number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        self._number_of_rooms = int(value) if value else 0

    @property
    def max_guests(self):
        return self._max_guests

    @max_guests.setter
    def max_guests(self, value):
        self._max_guests = int(value) if value else 0

    @property
    def tagline(self):
        return self._tagline

    @tagline.setter
    def tagline(self, value):
        self._tagline = value

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value

    @property
    def details(self):
        if not self._details:
            return []
        try:
            return json.loads(self._details)
        except (json.JSONDecodeError, TypeError):
            return []

    @details.setter
    def details(self, value):
        if isinstance(value, list):
            self._details = json.dumps(value)
        elif isinstance(value, str):
            self._details = value
        else:
            self._details = '[]'

    @property
    def rooms(self):
        if not self._rooms:
            return []
        try:
            return json.loads(self._rooms)
        except (json.JSONDecodeError, TypeError):
            return []

    @rooms.setter
    def rooms(self, value):
        if isinstance(value, list):
            self._rooms = json.dumps(value)
        elif isinstance(value, str):
            self._rooms = value
        else:
            self._rooms = '[]'

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value
    
    def to_dict(self):
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "status": self.status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "images": self.images,
            "number_of_rooms": self.number_of_rooms,
            "max_guests": self.max_guests,
            "tagline": self.tagline,
            "rules": self.rules,
            "details": self.details,
            "rooms": self.rooms,
            "location": self.location,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
