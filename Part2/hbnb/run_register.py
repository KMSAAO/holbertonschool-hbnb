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
    booking_service = BookingService()
    payment_service = PaymentService()
    refund_service = RefundServices()

    user = facade.register_user({
        "first_name": "Nawaf",
        "last_name": "Alzahrani",
        "email": "nawaf@example.com",
        "password": "A12345",
        "is_admin": True,
        "is_active": True
    })

    print("User registered with ID:", user.id)

    print("-------------------------------------------------------------------")

    place = facade.create_place({
        "title": "Cozy Cottage",
        "description": "A cozy cottage in the countryside.",
        "price": 120.00,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": user.id,
        "status": PlaceStatus.AVAILABLE,
        "amenity_status": PlaceAmenityStatus.ACTIVE
    })

    print("place name :", place.title, "place description :", place.description, "place price :", place.price, "place owner :", place.user.first_name + " " + place.user.last_name)

    print("-------------------------------------------------------------------")

    guest = facade.register_as_guest(user, "I love traveling and exploring new places.")

    print("Guest Info:", guest.id,guest.user.first_name + " " + guest.user.last_name, guest.bio)

    print("-------------------------------------------------------------------")



    booking = facade.create_booking({
        "guest": guest,
        "place": place,
        "Payment_id": None,
        "start_date": "2024-07-01",
        "end_date": "2024-07-05",
        "status": "pending"
    })

    print("Booking created with ID:", booking.id, "for Guest Name:", booking.place.user.first_name + " " + booking.place.user.last_name, "at Place :", booking.place.title)
    print("-------------------------------------------------------------------")

    payment = facade.create_payment({
        "book_id": booking.id,
        "booking": booking,
        "amount": booking.place.price * (booking.check_out - booking.check_in).days,
        "method_payment": "Credit Card",
        "status": "pending"
    })

    print("Payment created with ID:", payment.id, "for Booking :", payment.booking.place.title, "for Guest Name:", payment.booking.guest.user.first_name + " " + payment.booking.guest.user.last_name, "Amount:", payment.amount)
    print("-------------------------------------------------------------------")
