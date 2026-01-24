from app.models.base_model import BaseModel
from app.models.booking import Booking
from app.enums import payment_type, payment_status


class Payment(BaseModel):
    def __init__(self, book_id: str, booking: Booking, amount: float,
                 method_payment: payment_type, status: payment_status):
        super().__init__()
        self.book_id = book_id
        self.booking = booking
        self.amount = amount
        self.method_payment = method_payment
        self.status = status

    @property
    def book_id(self):
        return self._book_id

    @book_id.setter
    def book_id(self, value):
        if not isinstance(value, str):
            raise ValueError("book_id must be a string")
        self._book_id = value

    @property
    def booking(self):
        return self._booking

    @booking.setter
    def booking(self, value):
        if not isinstance(value, Booking):
            raise ValueError("booking must be an instance of Booking class")
        self._booking = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("amount must be a positive number")
        self._amount = float(value)

    @property
    def method_payment(self):
        return self._method_payment

    @method_payment.setter
    def method_payment(self, value):
        if not isinstance(value, payment_type):
            raise ValueError("method_payment must be an instance of payment_type Enum")
        self._method_payment = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, payment_status):
            raise ValueError("status must be an instance of payment_status Enum")
        self._status = value

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "amount": self.amount,
            "method_payment": self.method_payment.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
