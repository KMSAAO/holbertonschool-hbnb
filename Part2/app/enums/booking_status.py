from enum import Enum

class BookingStatus(Enum):

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELED = "canceled"
    NO_SHOW = "no_show"