from app.models.base_model import BaseModel
from app.enums import booking_status
from app.models.place import Place
from app.models.guest import Guest

class Booking(BaseModel):

    def __init__(self, guest:Guest, place:Place, payment_id, check_in, check_out, status: booking_status):
        super().__init__()
        self.guest = guest
        self.place = place
        self.payment_id = payment_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = status