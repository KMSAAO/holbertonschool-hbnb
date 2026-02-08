from datetime import datetime
from app.models.base_model import BaseModel
from app.enums.booking_status import BookingStatus
from app.db import db
from app.models.place import Place
from app.models.guest import Guest


class Booking(BaseModel):

    __tablename__ = "bookings"

    _guest_id = db.Column("guest_id", db.String(60), db.ForeignKey("guests.id"), nullable=False)
    _place_id = db.Column("place_id", db.String(60), db.ForeignKey("places.id"), nullable=False)
    _check_in = db.Column("check_in", db.DateTime, nullable=False)
    _check_out = db.Column("check_out", db.DateTime, nullable=False)
    _status = db.Column("status", db.Enum(BookingStatus), nullable=False)

    guest = db.relationship("Guest", backref="bookings", foreign_keys=[_guest_id])
    place = db.relationship("Place", backref="bookings", foreign_keys=[_place_id])

    def __init__(self, guest_id: str, place_id: str, check_in: datetime, check_out: datetime, status: BookingStatus):
        super().__init__()
        self.guest_id = guest_id
        self.place_id = place_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = status

    @property
    def guest_id(self):
        return self._guest_id

    @guest_id.setter
    def guest_id(self, value):
        if not isinstance(value, str):
            raise ValueError("guest_id must be a string")
        self._guest_id = value

    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, str):
            raise ValueError("place_id must be a string")
        self._place_id = value

    @property
    def check_in(self):
        return self._check_in

    @check_in.setter
    def check_in(self, value):
        if not isinstance(value, datetime):
            raise ValueError("check_in must be a datetime object")
        self._check_in = value

    @property
    def check_out(self):
        return self._check_out

    @check_out.setter
    def check_out(self, value):
        if not isinstance(value, datetime):
            raise ValueError("check_out must be a datetime object")
        if value <= self.check_in:
            raise ValueError("check_out must be after check_in")
        self._check_out = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, str):
            try:
                value = BookingStatus(value)
            except ValueError:
                raise ValueError(f"{value} is not a valid BookingStatus")
    
        if not isinstance(value, BookingStatus):
            raise ValueError("status must be an instance of BookingStatus enum")
    
        self._status = value

    def to_dict(self):
        return {
            "id": self.id,
            "guest_id": self.guest_id,
            "place_id": self.place_id,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
