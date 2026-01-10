from app.services.facade import HBnBFacade
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.enums.place_status import PlaceStatus
from app.enums.place_amenity_status import PlaceAmenityStatus
if __name__ == "__main__":
    facade = HBnBFacade()
    place_service = PlaceService()
    review_services = ReviewService()

    user = facade.register_user({
        "first_name": "Nawaf",
        "last_name": "Alzahrani",
        "email": "nawaf@example.com",
        "password": "A12345",
        "is_admin": True,
        "is_active": True
    })


    place = facade.create_place({
        "owner_id": user.id,
        "title": "Vila",
        "description": "nice",
        "price": 122,
        "status": PlaceStatus.AVAILABLE,
        "latitude": 24.774265,
        "longitude": 46.738586
    })


    is_logged = facade.login_user("nawaf@example.com", "A12345")
    if is_logged:
        print("Welcome back", f"{user.first_name} {user.last_name}")

    print(facade.get_place_info(place.id))
