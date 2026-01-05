from enum import Enum

class PlaceStatus(Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    UNAVAILABLE = "unavailable"