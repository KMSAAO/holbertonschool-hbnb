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
        
    def cancel_booking(self, booking_id: str, repo):

        booking = repo.get(booking_id)
        if not booking:
            raise ValueError("booking not found")
        
        booking.status = BookingStatus.CANCELLED
        return repo.update(booking)  
    
    def update_status(self, booking_id: str, new_status: BookingStatus, repo):


        booking = repo.get(booking_id)
        if not booking:
            raise ValueError("booking not found")
        
        if not isinstance(new_status, BookingStatus):
            try:
                new_status = BookingStatus(new_status)
            except Exception:
                raise ValueError("Invalid booking status")
        
        booking.status = new_status
        return repo.update(booking)
    
    def update_booking_dates(self, booking_id: str, new_check_in: datetime, new_check_out: datetime, repo):

        booking = repo.get(booking_id)
        if not booking:
            raise ValueError("booking not found")
        
        if not isinstance(new_check_in, datetime):
            raise ValueError("new_check_in must be a datetime object")
        
        if not isinstance(new_check_out, datetime):
            raise ValueError("new_check_out must be a datetime object")
        
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
            "Payment_id": booking.Payment_id,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "status": booking.status.value
        }
    
    def is_place_available(self, place_id: str, check_in: datetime, check_out: datetime, repo):

        bookings = repo.filter_by(place_id=place_id)

        for booking in bookings:
            if (check_in < booking.check_out and check_out > booking.check_in):
                return False
        
        return True