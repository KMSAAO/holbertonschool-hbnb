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

    def get(self, guest_id):
        return Guest.query.get(guest_id)

    def get_all(self):
        return Guest.query.all()

    def get_by_user_id(self, user_id):
        return Guest.query.filter_by(user_id=user_id).first()

    def update(self, guest_id, data):
        guest = self.get(guest_id)
        if not guest:
            return None
        for k, v in data.items():
            setattr(guest, k, v)
        db.session.commit()
        return guest

    def delete(self, guest_id):
        guest = self.get(guest_id)
        if not guest:
            return False
        db.session.delete(guest)
        db.session.commit()
        return True

    
class BookingRepository:
    def add(self, booking):
        db.session.add(booking)
        db.session.commit()
        return booking

    def get(self, booking_id):
        return Booking.query.get(booking_id)

    def get_all(self):
        return Booking.query.all()

    def get_by_guest_id(self, guest_id):
        return Booking.query.filter_by(guest_id=guest_id).all()

    def get_by_status(self, status):
        return Booking.query.filter_by(status=status).all()

    def update(self, booking_id, data):
        booking = self.get(booking_id)
        if not booking:
            return None
        for k, v in data.items():
            setattr(booking, k, v)
        db.session.commit()
        return booking

    def delete(self, booking_id):
        booking = self.get(booking_id)
        if not booking:
            return False
        db.session.delete(booking)
        db.session.commit()
        return True


