from app.models.booking import Booking
from app.enums.booking_status import BookingStatus
import datetime

class BookingService():

    def create_booking(self, booking_data: dict, repo):

        guest_id = booking_data.get('guest_id')
        if not guest_id or not isinstance(guest_id, str):
            raise ValueError("guest_id is required and must be a string")

        guest_id = repo.get(guest_id)
        if not guest_id:
            raise ValueError("guest not found")
        
        place_id  = booking_data.get('place_id')
        if not place_id or not isinstance(place_id, str):
            raise ValueError("place_id is required and must be a string")
        place_id = repo.get(place_id)
        if not place_id:
            raise ValueError("place_id not found")
        
        Payment_id  = booking_data.get('Payment_id')
        if not Payment_id or not isinstance(Payment_id, str):
            raise ValueError("Payment_id is required and must be a string")
        Payment_id = repo.get(Payment_id)
        if not Payment_id:
            raise ValueError("Payment_id not found")

        check_in = check_in.get('check_in')
        if not check_in or not isinstance(check_in, datetime):
            raise ValueError("check_out is required")
        
        check_out = check_out.get('check_out')
        if not check_out or not isinstance(check_out, datetime):
            raise ValueError("check_out is required")
        
        raw_status = booking_data.get('status')
        if isinstance(raw_status, BookingStatus):
            status = raw_status
        else:
            try:
                status = BookingStatus(raw_status)
            except Exception:
                raise ValueError("Invalid booking status")
            
            booking = Booking(
            guest_id,
            place_id,
            Payment_id,
            Payment_id,
            check_in,
            check_out,
            status)

            repo.add(booking)

            return booking

