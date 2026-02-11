from app.models.base_model import BaseModel
from app.models.booking import Booking
from app.db import db
from app.enums.payment_type import MethodPayment
from app.enums.payment_status import PaymentStatus


class Payment(BaseModel):
    __tablename__ = "payments"
    _book_id = db.Column("book_id", db.String(60), db.ForeignKey("bookings.id"), nullable=False)
    _amount = db.Column("amount", db.Float, nullable=False)
    _method_payment = db.Column("method_payment", db.Enum(MethodPayment), nullable=False)
    _status = db.Column("status", db.Enum(PaymentStatus), nullable=False)

    booking = db.relationship("Booking", backref="payment", foreign_keys=[_book_id])


    def __init__(self, booking_id: str, amount: float,method_payment: MethodPayment, status: PaymentStatus):
        super().__init__()
        self.booking_id = booking_id
        self.amount = amount
        self.method_payment = method_payment
        self.status = status

    @property
    def booking_id(self):
        return self._book_id

    @booking_id.setter
    def booking_id(self, value):
        if not isinstance(value, str):
            raise ValueError("booking_id must be a string")
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
        if not isinstance(value, MethodPayment):
            raise ValueError("method_payment must be an instance of MethodPayment Enum")
        self._method_payment = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, PaymentStatus):
            raise ValueError("status must be an instance of PaymentStatus Enum")
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
