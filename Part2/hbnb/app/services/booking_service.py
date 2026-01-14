from app.models.booking import Booking
from app.enums.booking_status import BookingStatus
from datetime import datetime

class BookingService():

    def create_booking(self, booking_data, repo, place_repo):

        guest = booking_data.get('guest')
        if not guest:
            raise ValueError("Invalid guest")
        

        place = booking_data.get('place')
        if not place:
                raise ValueError("Invalid place")
    

        payment_id  = None

        start_raw = booking_data.get("start_date")
        end_raw = booking_data.get("end_date")

        try:
            check_in = datetime.strptime(start_raw, "%Y-%m-%d")
            check_out = datetime.strptime(end_raw, "%Y-%m-%d")
        except Exception:
            raise ValueError("start_date and end_date must be in format YYYY-MM-DD")
        
        raw_status = booking_data.get('status')

        if isinstance(raw_status, BookingStatus):
            status = raw_status
        else:
            try:
                status = BookingStatus(raw_status)
            except Exception:
                raise ValueError("Invalid booking status")

        booking = Booking(
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
    
    def update_booking_payment(self, booking_id: str, new_status: BookingStatus, repo):


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
            "status": booking.status.name
        }
    
    def is_place_available(self, place_id: str, check_in: datetime, check_out: datetime, repo):

        bookings = repo.filter_by(place_id=place_id)

        for booking in bookings:
            if (check_in < booking.check_out and check_out > booking.check_in):
                return False
        
        return True