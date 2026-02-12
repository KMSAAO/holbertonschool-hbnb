from app.models.base_model import BaseModel
from app.enums import payment_type, payment_status
from app.models.payment import Payment


class Refund(BaseModel):
    def __init__(self, payment_id: str, payment: Payment, amount_refund: float,
                 method_payment: payment_type, status: payment_status):
        super().__init__()
        self.payment_id = payment_id
        self.payment = payment
        self.amount_refund = amount_refund
        self.method_payment = method_payment
        self.status = status

    @property
    def payment_id(self):
        return self._payment_id

    @payment_id.setter
    def payment_id(self, value):
        if not isinstance(value, str):
            raise ValueError("payment_id must be a string")
        self._payment_id = value

    @property
    def payment(self):
        return self._payment

    @payment.setter
    def payment(self, value):
        if not isinstance(value, Payment):
            raise ValueError("payment must be an instance of Payment class")
        self._payment = value

    @property
    def amount_refund(self):
        return self._amount_refund

    @amount_refund.setter
    def amount_refund(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("amount_refund must be a positive number")
        self._amount_refund = float(value)

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
            "payment_id": self.payment_id,
            "amount_refund": self.amount_refund,
            "method_payment": self.method_payment.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
