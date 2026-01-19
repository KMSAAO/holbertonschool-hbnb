from enum import Enum

class RefundStatus(Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    DECLINED = "declined"
    COMPLETED = "completed"
    PARTIAL = "partial"