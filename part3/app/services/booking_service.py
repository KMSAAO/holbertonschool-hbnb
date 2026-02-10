from datetime import datetime
from flask_jwt_extended import current_user
from app.models.booking import Booking
from app.enums.booking_status import BookingStatus

class BookingService:

    def create_booking(self, booking_data, guest_repo, booking_repo, place_repo, current_user):

        guest = guest_repo.get_by_user_id(current_user)

        if guest is None:
            raise ValueError("Guest not found for current user")


        place = place_repo.get_available_place_by_status("available")
        if not place:
            raise ValueError("There are no available places for booking")

        try:
            check_in = datetime.strptime(booking_data.get("check_in"), "%Y-%m-%d")
            check_out = datetime.strptime(booking_data.get("check_out"), "%Y-%m-%d")
        except Exception:
            raise ValueError("check_in and check_out must be in format YYYY-MM-DD")

        raw_status = booking_data.get('status', BookingStatus.PENDING)
        try:
            status = raw_status if isinstance(raw_status, BookingStatus) else BookingStatus(raw_status)
        except Exception:
            raise ValueError("Invalid booking status")


        
        booking = Booking(
            guest_id=guest.id,
            place_id=place.id,
            check_in=check_in,
            check_out=check_out,
            status=status
        )

        place.status = "booked"


        booking_repo.add(booking)
        return booking
    
    def get_all_bookings(self, booking_repo, guest_repo, user_repo, current_user):

        user = user_repo.get(current_user)
        if not user:
            return []

        if user.is_admin:
            return booking_repo.get_all_bookings()

        guest = guest_repo.get_by_user_id(current_user)
        if not guest:
            return []

        return booking_repo.get_bookings_by_guest_id(guest.id)

    def get_booking_by_id(self, booking_id: str, current_user, booking_repo, user_repo, guest_repo):

        booking = booking_repo.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        user = user_repo.get(current_user)
        if not user:
            raise PermissionError("Forbidden")

        if user.is_admin:
            return booking

        guest = guest_repo.get_by_user_id(current_user)
        if not guest or booking.guest_id != guest.id:
            raise PermissionError("Forbidden")

        return booking
    
    def get_bookings_by_guest_id(self, guest_id: str, current_user, booking_repo, user_repo, guest_repo):

        user = user_repo.get(current_user)
        if not user:
            raise PermissionError("Forbidden")

        if user.is_admin:
            return booking_repo.get_bookings_by_guest_id(guest_id)

        guest = guest_repo.get_by_user_id(current_user)
        if not guest or guest.id != guest_id:
            raise PermissionError("Forbidden")

        bookings = booking_repo.get_bookings_by_guest_id(guest_id)
        return bookings or []