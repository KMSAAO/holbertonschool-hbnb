from models.base_model import BaseModel
from app.enums import payment_type, payment_status

class Payment_id(BaseModel):

    def __init__(self, book_id, amount, method_payment: payment_status, status: payment_status, paid_at):
        super().__init__()

        self.book_id = book_id
        self.amount = amount
        self.method_payment = method_payment
        self.status = status
        self.paid = paid_at