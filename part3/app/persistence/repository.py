from abc import ABC, abstractmethod
from app.db import db
from app.models.user import User
from app.models.guest import Guest
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.refund import Refund


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, value):
        pass

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return True

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return False

        for key, value in data.items():
            setattr(obj, key, value)

        db.session.commit()
        return True

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False

        db.session.delete(obj)
        db.session.commit()
        return True
    
    def get_active_places(self):
        return self.model.query.filter(self.model._status == "active").all()

    def get_by_attribute(self, attr_name, value):
        return self.model.query.filter_by(**{attr_name: value}).first()
    
    def commit(self):
        db.session.commit()

# class UserRepository:
#     def __init__(self, model):
#         self.model = model

#     def add(self, user):
#         db.session.add(user)
#         db.session.commit()
#         return user

#     def get(self, user_id):
#         return User.query.get(user_id)

#     def get_all(self):
#         return User.query.all()

#     def get_by_email(self, email):
#         return User.query.filter_by(email=email).first()

#     def update(self, user_id, data):
#         user = self.get(user_id)
#         if not user:
#             return None
#         for k, v in data.items():
#             setattr(user, k, v)
#         db.session.commit()
#         return user

#     def delete(self, user_id):
#         user = self.get(user_id)
#         if not user:
#             return False
#         db.session.delete(user)
#         db.session.commit()
#         return True
    
class GuestRepository:
    def add(self, guest):
        if not guest or not hasattr(guest, "user_id"):
            raise ValueError("Guest must have a valid user_id")
        db.session.add(guest)
        db.session.commit()
        return guest

    def get_by_user_id(self, user_id):
        return Guest.query.filter_by(user_id=user_id).first()

    def get(self, guest_id):
        return Guest.query.filter_by(guest_id).all

    def get_all(self):
        return Guest.query.all()

    
class BookingRepository:
    def __init__(self):
        self.model = Booking

    def add(self, booking):
        db.session.add(booking)
        db.session.commit()
        return booking
    
    def get_all_bookings(self):
        return Booking.query.all()

    def get_booking_by_id(self, booking_id):
        return Booking.query.get(booking_id)

    def get_bookings_by_guest_id(self, guest_id: str):
        return Booking.query.filter_by(_guest_id=guest_id).all()
    
    def update_booking_status(self, booking_id, new_status):
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("booking not found")

        booking._status = new_status
        db.session.commit()
        return booking
    
    def has_overlapping_booking(self, place_id, check_in, check_out):
        return self.model.query.filter(
            self.model._place_id == place_id,
            self.model._check_in < check_out,
            self.model._check_out > check_in
        ).first() is not None


class PaymentRepository:

    def __init__(self):
        self.model = Payment
    
    def add(self, payment):
        db.session.add(payment)
        db.session.commit()
        return payment
    
    def get_payment_by_id(self, payment_id):
        return self.model.query.get(payment_id)
    
    def get_payment_by_booking_id(self, booking_id):
        return self.model.query.filter_by(_booking_id=booking_id).all()
    
    def get_all_payments(self):
        return self.model.query.all()
    
    def update_payment_status(self, payment_id, new_status):
        payment = self.get_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        payment._status = new_status
        db.session.commit()
        return payment

class RefundRepository:
    def __init__(self):
        self.model = Refund

    def add(self, refund):
        db.session.add(refund)
        db.session.commit()
        return refund
    
    def get_refund_by_id(self, refund_id):
        return self.model.query.get(refund_id)
    
    def get_refund_by_payment_id(self, payment_id):
        return self.model.query.filter_by(payment_id=payment_id).first()
    
    def get_refunds_by_payment_id(self, payment_id):
        return self.model.query.filter_by(payment_id=payment_id).all()
    
    def get_all_refunds(self):
        return self.model.query.all()
    
    def update_refund_status(self, refund_id, new_status):
        refund = self.get_refund_by_id(refund_id)
        if not refund:
            raise ValueError("Refund not found")

        refund._status = new_status
        db.session.commit()
        return refund
