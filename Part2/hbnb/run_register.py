from app.services.facade import HBnBFacade
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.guest_service import GuestService
from app.services.booking_service import BookingService
from app.services.payment_service import PaymentService
from app.services.refund_service import RefundServices


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

    user_info = facade.get_user(user)
    print("User Info:", user_info)
    place = facade.create_place({
        "name": "Cozy Cottage",
        "description": "A cozy cottage in the countryside.",
        "owner_id": user,
        "status": PlaceStatus.AVAILABLE,
        "amenity_status": PlaceAmenityStatus.FULLY_FURNISHED
    })
    print("Place Created:", place.id)
    
