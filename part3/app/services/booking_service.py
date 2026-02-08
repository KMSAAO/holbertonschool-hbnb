from datetime import datetime
from app.models.booking import Booking
from app.enums.booking_status import BookingStatus


class BookingService:

    def create_booking(self, booking_data, repo, place_repo):
        guest_id = booking_data.get('guest_id')
        if not guest_id:
            raise ValueError("Invalid guest_id")

        place_id = booking_data.get('place_id')
        if not place_id:
            raise ValueError("Invalid place_id")

        try:
            check_in = datetime.strptime(booking_data.get("check_in"), "%Y-%m-%d")
            check_out = datetime.strptime(booking_data.get("check_out"), "%Y-%m-%d")
        except Exception:
            raise ValueError("check_in and check_out must be in format YYYY-MM-DD")

        raw_status = booking_data.get('status')
        try:
            status = raw_status if isinstance(raw_status, BookingStatus) else BookingStatus(raw_status)
        except Exception:
            raise ValueError("Invalid booking status")

        booking = Booking(
            guest_id,
            place_id,
            check_in,
            check_out,
            status
        )

        repo.add(booking)
        return booking
    
    def get_all_bookings(self, repo):
        all_bookings = repo.get_all_bookings()
        if not all_bookings:
            raise ValueError("No bookings found")
        return all_bookings

    def get_booking_by_id(self, booking_id, repo):
        booking_id = repo.get_booking_by_id(booking_id)
        if not booking_id:
            raise ValueError("Booking not found")
        return booking_id
    
    def get_bookings_by_guest_id(self, guest_id: str, repo):
        
        bookings = repo.get_bookings_by_guest_id(guest_id)
        if not bookings:
            raise ValueError("No bookings found for this guest")
        return bookings
    
    def update_booking_status(self, booking_id: str, new_status: str, repo):
        booking = Booking.query.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        booking.status = new_status

        repo.update_booking_status(booking_id, new_status)

        return booking.status