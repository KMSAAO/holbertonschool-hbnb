from enum import Enum

class PaymentStatus(Enum):
    
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"

