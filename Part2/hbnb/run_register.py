from app.services.facade import HBnBFacade
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.guest_service import GuestService

from app.enums.place_status import PlaceStatus
from app.enums.place_amenity_status import PlaceAmenityStatus

if __name__ == "__main__":
    facade = HBnBFacade()
    place_service = PlaceService()
    review_services = ReviewService()
    guest_service = GuestService()
    


    user = facade.register_user({
        "first_name": "Nawaf",
        "last_name": "Alzahrani",
        "email": "nawaf@example.com",
        "password": "A12345",
        "is_admin": True,
        "is_active": True
    })

