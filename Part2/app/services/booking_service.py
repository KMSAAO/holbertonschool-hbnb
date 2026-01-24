from datetime import datetime
from app.models.booking import Booking
from app.enums.booking_status import BookingStatus


class BookingService:

    def create_booking(self, booking_data, repo, place_repo):
        guest = booking_data.get('guest')
        if not guest:
            raise ValueError("Invalid guest")

        place = booking_data.get('place')
        if not place:
            raise ValueError("Invalid place")

        payment_id = None

        try:
            check_in = datetime.strptime(booking_data.get("start_date"), "%Y-%m-%d")
            check_out = datetime.strptime(booking_data.get("end_date"), "%Y-%m-%d")
        except Exception:
            raise ValueError("start_date and end_date must be in format YYYY-MM-DD")

        raw_status = booking_data.get('status')
        try:
            status = raw_status if isinstance(raw_status, BookingStatus) else BookingStatus(raw_status)
        except Exception:
            raise ValueError("Invalid booking status")

        booking = Booking(
            guest.id,
            place.id,
            guest,
            place,
            payment_id,
            check_in,
            check_out,
            status
        )

        repo.add(booking)
        return booking

    def cancel_booking(self, booking_id: str, repo):
        booking = repo.get(booking_id)
        if not booking:
            raise ValueError("booking not found")

        booking.status = BookingStatus.CANCELLED
        return repo.update(booking)

    def update_booking_payment(self, booking_id: str, payment_id: str, new_status: BookingStatus, repo):
        booking = repo.get(booking_id)
        if not booking:
            raise ValueError("booking not found")

        booking.payment_id = payment_id

        try:
            booking.status = new_status if isinstance(new_status, BookingStatus) else BookingStatus(new_status)
        except Exception:
            raise ValueError("Invalid booking status")

        return repo.update(booking)

    def update_booking_dates(self, booking_id: str, new_check_in: datetime, new_check_out: datetime, repo):
        booking = repo.get(booking_id)
        if not booking:
            raise ValueError("booking not found")

        # تمت إزالة التحقق من النوع والمنطق، لأنها مفروض تتم داخل model.setter
        booking.check_in = new_check_in
        booking.check_out = new_check_out

        return repo.update(booking)

    def get_booking_info(self, booking_id: str, repo):
        booking = repo.get(booking_id)
        if not booking:
            raise ValueError("booking not found")

        return {
            "booking_id": booking.id,
            "guest_id": booking.guest_id,
            "place_id": booking.place_id,
            "payment_id": booking.payment_id,
            "check_in": booking.check_in.isoformat(),
            "check_out": booking.check_out.isoformat(),
            "status": booking.status.name
        }

    def is_place_available(self, place_id: str, check_in: datetime, check_out: datetime, repo):
        bookings = repo.filter_by(place_id=place_id)

        for booking in bookings:
            if (check_in < booking.check_out and check_out > booking.check_in):
                return False

        return True

    def get_all_bookings(self, repo):
        all_bookings = repo.get_all()
        if not all_bookings:
            return None

        return all_bookings