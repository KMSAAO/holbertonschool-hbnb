from app.services.facade import HBnBFacade
from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.guest_service import GuestService
from app.services.booking_service import BookingService
from app.services.payment_service import PaymentService
from app.services.refund_service import RefundServices
from app.services.payment_service import PaymentService
from app.services.amenity_service import AmenityService


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
    payment_service = PaymentService()
    amenity_service = AmenityService()

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

    print("Booking created with ID:", booking.id, "for Guest Name:", booking.place.user.first_name + " " + booking.place.user.last_name, "at Place :", booking.place.title, "with Payment ID:", booking.payment_id,"status:", booking.status.name)
    print("-------------------------------------------------------------------")

    payment = facade.create_payment({
        "book_id": booking.id,
        "booking": booking,
        "amount": booking.place.price * (booking.check_out - booking.check_in).days,
        "method_payment": "Credit Card",
        "status": "pending"
    })

    print("Payment created with ID:", payment.id, "for Booking :", payment.booking.place.title, "for Guest Name:", payment.booking.guest.user.first_name + " " + payment.booking.place.user.last_name, "Amount:", payment.amount)
    print("-------------------------------------------------------------------")

    booking = facade.update_booking_payment(booking.id, payment.id, "confirmed")

    print("Booking created with ID:", booking.id, "for Guest Name:", booking.place.user.first_name + " " + booking.place.user.last_name, "at Place :", booking.place.title, "with Payment ID:", booking.payment_id,"status:", booking.status.name, )
    print("-------------------------------------------------------------------")


    refund_service = facade.create_refund({
        "payment_id": payment.id,
        "payment": payment,
        "amount_refund": payment.amount,
        "method_payment": "Credit Card",
        "status": "requested",
    })

    print("Refund created with ID:", refund_service.id,"Owner account: ", payment.booking.guest.user.first_name + " " + payment.booking.guest.user.last_name, "for Payment ID:", refund_service.payment_id, "Amount Refund:", refund_service.amount_refund, "Status:", refund_service.status.name)

    print("-------------------------------------------------------------------")
    
    amenity = facade.create_amenity({
    "amenity_name": "WiFi",
    "description": "High-speed wireless internet access.",
    "status": PlaceAmenityStatus.ACTIVE
})


    print("Amenity created with ID:", amenity.id, "Name:", amenity.amenity_name, "Description:", amenity.description)

    print("-------------------------------------------------------------------")

    place_amenity = facade.place_amenity_service.add_amenity_to_place(
        place_id=place.id,
        amenity_id= amenity.id,
        repo=facade.place_amenity_repo
    )  

    print("PlaceAmenity created with ID:", place_amenity.id, "for Place ID:", place_amenity.place_id, "with Amenity ID:", place_amenity.amenity_id, "Status:", place_amenity.status.name)

    print("-------------------------------------------------------------------")

    review = facade.create_review({
        "place": place.id,
        "guest": guest.id,
        "rating": 5,
        "comment": "Amazing place! Had a wonderful time."
    })

    print("Review created with ID:", review.id, "for Place ID:", review.place.id, "by Guest Name:", review.guest.user.first_name + " " + review.guest.user.last_name, "Rating:", review.rating, "Comment:", review.comment)
    print("-------------------------------------------------------------------")