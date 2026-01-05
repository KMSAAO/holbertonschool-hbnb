from app.models.base_model import BaseModel
from app.enums import payment_type, payment_status

class Refund(BaseModel):

    def __init__(self, payment_id, amount_refund, method_payment: payment_type, status: payment_status):
        super().__init__()

        self.payment_id = payment_id
        self.amount_refund = amount_refund
        self.method_payment = method_payment
        self.status = status