from datetime import datetime
from app.models.base_model import BaseModel
from app.enums import booking_status
from app.models.place import Place
from app.models.guest import Guest


class Booking(BaseModel):
    def __init__(self, guest_id: str, place_id: str, guest: Guest, place: Place,
                 payment_id: str, check_in: datetime, check_out: datetime, status: booking_status):
        super().__init__()
        self.guest_id = guest_id
        self.place_id = place_id
        self.guest = guest
        self.place = place
        self.payment_id = payment_id
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
    def guest(self):
        return self._guest

    @guest.setter
    def guest(self, value):
        if not isinstance(value, Guest):
            raise ValueError("guest must be a Guest instance")
        self._guest = value

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, value):
        if not isinstance(value, Place):
            raise ValueError("place must be a Place instance")
        self._place = value

    @property
    def payment_id(self):
        return self._payment_id

    @payment_id.setter
    def payment_id(self, value):
        if not isinstance(value, str):
            raise ValueError("payment_id must be a string")
        self._payment_id = value

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
        if not isinstance(value, booking_status):
            raise ValueError("status must be an instance of booking_status enum")
        self._status = value

    def to_dict(self):
        return {
            "id": self.id,
            "guest_id": self.guest_id,
            "place_id": self.place_id,
            "payment_id": self.payment_id,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
