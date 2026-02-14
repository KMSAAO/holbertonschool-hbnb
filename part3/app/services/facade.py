from app.persistence.repository import SQLAlchemyRepository
from app.persistence.repository import GuestRepository, BookingRepository

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

from app.services.user_service import UserServices
from app.services.place_service import PlaceService
from app.services.amenity_service import AmenityService
from app.services.review_service import ReviewService
from app.services.guest_service import GuestService
from app.services.booking_service import BookingService
# from app.services.payment_service import PaymentService
# from app.services.refund_service import RefundServices
# from app.services.place_amenity import PlaceAmenityService


class HBnBFacade:
    def __init__(self):
        self.repos_init()
        self.service_init()

    def repos_init(self):
        """Repositories Initialization"""
        self.user_db = SQLAlchemyRepository(User)
        self.place_db = SQLAlchemyRepository(Place)
        self.review_db = SQLAlchemyRepository(Review)
        self.amenity_db = SQLAlchemyRepository(Amenity)
        self.guest_db = GuestRepository()
        self.booking_db = BookingRepository()
        # self.payment_db = SQLAlchemyRepository()
        # self.refund_db = SQLAlchemyRepository()
        # self.place_amenity_db = SQLAlchemyRepository()

    def service_init(self):
        """Services Initialization"""
        self.user_service = UserServices()
        self.place_service = PlaceService()
        self.review_service = ReviewService()
        self.amenity_service = AmenityService()
        self.guest_service = GuestService()
        self.booking_service = BookingService()
        # self.payment_service = PaymentService()
        # self.refund_service = RefundServices()
        # self.place_amenity_service = PlaceAmenityService()

    
    #user methods

    def create_user(self, user_data: dict) -> str:
        return self.user_service.create_user(user_data, self.user_db)

    def login_user(self, email: str, password: str) -> bool:
        return self.user_service.login(email, password, self.user_db)

    def get_user(self, user_id: str) -> dict:
        return self.user_service.get_user_info(user_id, self.user_db)

    def get_by_attribute(self, attr_name, value):
        return self.user_service.get_by_attribute(attr_name, value, self.user_db)

    def get_user_by_email(self, email: str):
        return self.get_by_attribute("email", email)

    def update_user(self, user_id: str, user_data: dict) -> bool:
        return self.user_service.update_user(user_id, user_data, self.user_db)

    def delete_user(self, user_id: str) -> bool:
        return self.user_service.delete_user(user_id, self.user_db, self.place_db)

    def get_all_users(self):
        return self.user_service.get_all_users(self.user_db)
    
    
    
    #place methods

    def create_place(self, place_data: dict):
        return self.place_service.create_place(
            place_data=place_data,
            repo=self.place_db,
            user_db=self.user_db,
            amenity_repo=self.amenity_db
        )

    def get_place(self, place_id):
        place = self.place_service.get_place(place_id, self.place_db)
        if place:
            # Manually populate reviews for in-memory repository
            all_reviews = self.review_service.get_all_reviews(self.review_db)
            if all_reviews:
                place.reviews = [r for r in all_reviews if r.place_id == place_id]
            
            if all_reviews:
                place.reviews = [r for r in all_reviews if r.place_id == place_id]
        return place

    def get_place_info(self, place_id: str) -> dict:
        return self.place_service.get_place_info(
            place_id=place_id,
            place_repo=self.place_db
        )

    def update_place(self, place_id: str, place_data: dict) -> bool:
        updated = self.place_service.update_place(
            place_id=place_id,
            place_data=place_data,
            place_repo=self.place_db
        )

        if updated:
            self.place_db.commit()

        return updated

    def get_all_places(self):
        return self.place_service.get_all_places(self.place_db)

    def delete_place(self, place_id: str) -> bool:
        return self.place_service.delete_place(
            place_id=place_id,
            place_repo=self.place_db
        )
    
    #review methods

    def create_review(self, review_data: dict):
        return self.review_service.create_Review(
            review_data,
            place_repo=self.place_db,
            review_repo=self.review_db
        )

    def get_review_info(self, review_id: str) -> dict:
        return self.review_service.get_review_info(
            review_id=review_id,
            review_repo=self.review_db
        )

    def update_review(self, review_id: str, review_data: dict) -> bool:
        updated_review = self.review_service.update_review(
            review_id,
            review_data,
            self.review_db
        )
        self.review_db.commit()
        return updated_review

    def delete_review(self, review_id: str) -> bool:
        return self.review_service.delete_Review(
            review_id, self.review_db
        )
    
    def get_all_reviews(self):
        reviews = self.review_db.get_all()
        if not reviews:
            return []
        return reviews
    
    #amenity methods

    def create_amenity(self, amenity_data: dict):
        return self.amenity_service.create_amenity(
            amenity_data,
            self.amenity_db
        )

    def get_amenity_info(self, amenity_id: str) -> dict:
        return self.amenity_service.get_amenity_info(
            amenity_id,
            self.amenity_db
        )

    def update_amenity(self, amenity_id: str, amenity_data: dict) -> bool:
        return self.amenity_service.update_amenity(
            amenity_id,
            amenity_data,
            self.amenity_db
        )

    def get_all_amenities(self):
        return self.amenity_service.get_all_amenities(
            self.amenity_db
        )

    def delete_amenity(self, amenity_id: str) -> bool:
        return self.amenity_service.delete_amenity(
            amenity_id,
            self.amenity_db
        )

    #guest methods
    def register_as_guest(self, user_data: dict, bio=""):
        user = user_data
        return self.guest_service.register_as_guest(user, self.guest_db, bio)


    def get_guest_info(self, guest_id):
        return self.guest_service.get_guest_info(guest_id, self.guest_db)
    
    #booking methods

    def create_booking(self, booking_data: dict):
        return self.booking_service.create_booking(booking_data, self.booking_db, self.place_db)
    
    def get_all_bookings(self):
        return self.booking_service.get_all_bookings(self.booking_db)

    def get_bookings_by_id(self, booking_id):
        return self.booking_service.get_booking_by_id(booking_id, self.booking_db)
    
    def get_bookings_by_guest_id(self, guest_id: str):
        return self.booking_service.get_bookings_by_guest_id(guest_id, self.booking_db)
    
    def update_booking_status(self, booking_id: str, status: str):
        return self.booking_service.update_booking_status(booking_id, status, self.booking_db)

    #payment methods

    def create_payment(self, payment: dict):
        return self.payment_service.create_payment(
            payment,
            repo=self.payment_db,
            booking_repo=self.booking_db
        )

    def get_payment_info(self, payment_id: str) -> dict:
        return self.payment_service.get_payment_info(
            payment_id,
            repo=self.payment_db
        )

    def update_payment_status(self, payment_id: str, status: str) -> bool:
        pass

    def delete_payment(self, payment_id: str) -> bool:
        pass

    #refund methods
    def create_refund(self, refund_data: dict):
        return self.refund_service.create_refund(
            refund_data,
            repo=self.refund_db,
            payment_repo=self.payment_db
        )

    def update_refund(self, refund_id: str, status: str):
        return self.refund_service.update_payment(
            refund_id,
            status,
            repo=self.refund_db
        )

    def get_refund_info(self, refund_id: str) -> dict:
        pass

    def delete_refund(self, refund_id: str) -> bool:
        pass

    def get_refund_info_by_payment_id(self, payment_id: str) -> dict:
        pass

    #place-amenity methods

    def add_amenity_to_place(self, place_id: str, amenity_id: str):
        return self.place_service.add_amenity(
            place_id,
            amenity_id,
            place_repo=self.place_db,
            amenity_repo=self.amenity_db
        )

    def remove_amenity_from_place(self, place_id: str, amenity_id: str):
        return self.place_service.remove_amenity(
            place_id,
            amenity_id,
            place_repo=self.place_db,
            amenity_repo=self.amenity_db
        )

    def get_place_amenity_info(self, place_amenity_id: str) -> dict:
        return self.place_amenity_service.get_place_amenity_info(
            place_amenity_id,
            repo=self.place_amenity_db
        )

    def update_place_amenity_status(self, place_amenity_id: str, status: str) -> bool:
        return self.place_amenity_service.update_place_amenity_status(
            place_amenity_id,
            status,
            repo=self.place_amenity_db
        )
