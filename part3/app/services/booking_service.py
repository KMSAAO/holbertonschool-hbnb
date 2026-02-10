from datetime import datetime
from app.models.booking import Booking
from app.enums.booking_status import BookingStatus

class BookingService:

    def create_booking(self, booking_data, guest_repo, booking_repo, place_repo, current_user):

        guest = guest_repo.get_by_user_id(current_user)
        if not guest:
            raise ValueError("Guest not found")

        try:
            check_in = datetime.strptime(booking_data["check_in"], "%Y-%m-%d")
            check_out = datetime.strptime(booking_data["check_out"], "%Y-%m-%d")
        except Exception:
            raise ValueError("Invalid date format")

        if check_in >= check_out:
            raise ValueError("check_out must be after check_in")

        available_place_ids = self.get_available_place_ids(
            check_in, check_out, place_repo, booking_repo
        )

        if not available_place_ids:
            raise ValueError("No available places for selected dates")

        place_id = available_place_ids[0]

        booking = Booking(
            guest_id=guest.id,
            place_id=place_id,
            check_in=check_in,
            check_out=check_out,
            status=BookingStatus.CONFIRMED
        )

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
    
    def get_available_place_ids(self, check_in, check_out, place_repo, booking_repo):

        available_place_ids = []

        active_places = place_repo.get_active_places()

        for place in active_places:
            overlapping = booking_repo.has_overlapping_booking(
            place.id, check_in, check_out
            )
        
            print(f"Checking place ID {place.id}: Overlapping booking: {overlapping}")  # Debug statement
            if not overlapping:
                available_place_ids.append(place.id)

        return available_place_ids