from app.models.base_model import BaseModel
from app.models.booking import Booking
from app.enums import payment_type, payment_status

class Payment(BaseModel):

    def __init__(self, book_id, booking: Booking, amount, method_payment: payment_type, status: payment_status):
        super().__init__()

        self.book_id = book_id
        self.booking = booking
        self.amount = amount
        self.method_payment = method_payment
        self.status = status