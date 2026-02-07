from abc import ABC, abstractmethod
from app.db import db

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

class UserRepository(SQLAlchemyRepository):

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
    
class GuestRepository(SQLAlchemyRepository):
    def get_guest_by_user_id(self, user_id):
        return self.model.query.filter_by(user_id=user_id).first()

    def add(self, guest):
        if not guest or not hasattr(guest, "user_id"):
            raise ValueError("Guest must have a valid user_id")

        db.session.add(guest)
        db.session.commit()
        return guest
    
class BookingRepository(SQLAlchemyRepository):
    def get_all_bookings(self):
        return self.model.query.all()

