from abc import ABC, abstractmethod
from app.db import db
from app.models.user import User
from app.models.guest import Guest
from app.models.booking import Booking


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
    
    def get_available_place_by_status(self, status):
        return self.model.query.filter_by(_status=status).all()

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

        booking.status = new_status
        db.session.commit()
        return booking
    
