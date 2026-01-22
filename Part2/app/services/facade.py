from app.persistence.repository import InMemoryRepository
from app.services.user_service import UserServices
from app.services.place_service import PlaceService
from app.services.amenity_service import AmenityService
from app.services.review_service import ReviewService
from app.services.guest_service import GuestService
from app.services.booking_service import BookingService
from app.services.payment_service import PaymentService
from app.services.refund_service import RefundServices
from app.services.place_amenity import PlaceAmenityService

class HBnBFacade:
    def __init__(self):

        self.repos_init()
        self.service_init()

    def repos_init(self):
        """Repositories Initialization"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.guest_repo = InMemoryRepository()
        self.booking_repo = InMemoryRepository()
        self.payment_repo = InMemoryRepository()
        self.refund_repo = InMemoryRepository()
        self.place_amenity_repo = InMemoryRepository()

    def service_init(self):
        """Services Initialization"""
        self.user_service = UserServices()
        self.place_service = PlaceService()
        self.review_service = ReviewService()
        self.amenity_service = AmenityService()
        self.guest_service = GuestService()
        self.booking_service = BookingService()
        self.payment_service = PaymentService()
        self.refund_service = RefundServices()
        self.place_amenity_service = PlaceAmenityService()
    
    """User Methods"""
    def register_user(self, user_data: dict) -> str:

        return self.user_service.register_users(user_data, self.user_repo)

    def login_user(self, email: str, password: str) -> bool:
        return self.user_service.login(email, password, self.user_repo)

    def get_user(self, user_id: str) -> dict:

        return self.user_service.get_user_info(user_id, self.user_repo)

    def update_user(self, user_id: str, user_data: dict) -> bool:
        
        return self.user_service.update_user(user_id, user_data, self.user_repo)
    
    def delete_user(self, user_id: str) -> bool:

        return self.user_service.delete_user(user_id, self.user_repo, self.place_repo)
    
    def get_all_users(self):
        return self.user_service.get_all_users(self.user_repo)
    
    """Place Methods"""
    def create_place(self, place_data: dict):

        return self.place_service.create_place(
            place_data=place_data,
            repo=self.place_repo,
            user_repo=self.user_repo
        )

    def get_place_info(self, place_id: str) -> dict:

        return self.place_service.get_place_info(
            place_id=place_id,
            place_repo=self.place_repo
        )

    def update_place(self, place_id: str, place_data: dict) -> bool:

        return self.place_service.update_place(
            place_id=place_id,
            place_data=place_data,
            place_repo=self.place_repo
        )

    def get_all_places(self):
        return self.place_service.get_all_places(self.place_repo)

    def delete_place(self, place_id: str) -> bool:

        return self.place_service.delete_place(
            place_id=place_id,
            place_repo=self.place_repo
        )

    """review Methods"""
    def create_review(self, review_data: dict):
        return self.review_service.create_Review(
            review_data,
            place_repo=self.place_repo,
            review_repo=self.review_repo
        )


    def get_review_info(self, review_id: str) -> dict:
        return self.review_service.get_review_info(
            review_id=review_id,
            review_repo=self.review_repo
        )

    def update_review(self, review_id: str, review_data: dict) -> bool:
        return self.review_service.update_review(
            review_id,
            review_data,
            self.review_repo
        )
    
    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        if not reviews:
            return []
        return reviews

    def delete_review(self, review_id: str) -> bool:
        return self.review_service.delete_Review(
            review_id, self.review_repo
        )


    """Amenity Methods"""
    def create_amenity(self, amenity_data: dict):
        return self.amenity_service.create_amenity(
            amenity_data,
            self.amenity_repo
        )

    def get_amenity_info(self, amenity_id: str) -> dict:
        return self.amenity_service.get_amenity_info(
            amenity_id,
            self.amenity_repo
        )

    def update_amenity(self, amenity_id: str, amenity_data: dict) -> bool:
        return self.amenity_service.update_amenity(
            amenity_id,
            amenity_data,
            self.amenity_repo
        )
    
    def get_all_amenities(self):
        return self.amenity_service.get_all_amenities(
            self.amenity_repo
        )

    def delete_amenity(self, amenity_id: str) -> bool:

        return self.amenity_service.delete_amenity(
            amenity_id,
            self.amenity_repo
        )
    
    """guest methods"""
    def register_as_guest(self, user, bio=""):

        return self.guest_service.register_as_guest(user, self.guest_repo, bio)
    
    def get_guest_info(self, guest_id):

        return self.guest_service.get_guest_info(guest_id, self.guest_repo)
    
    """Booking Methods"""
    def create_booking(self, booking_data: dict):

        return self.booking_service.create_booking(
            booking_data,
            self.booking_repo,
            place_repo=self.place_repo,

        )
    
    def cancel_booking(self, booking_id: str):
        return self.booking_service.cancel_booking(
            booking_id,
            repo=self.place_repo
        )
    
    def get_booking_info(self, booking_id: str):
        return self.booking_service.get_booking_info(
            booking_id,
            repo=self.place_repo
        )
    
    def update_booking_dates(self, booking_id: str, booking_data: dict):
        return self.booking_service.update_booking_dates(
            booking_id,
            booking_data,
            repo=self.place_repo
        )
    
    def update_status(self, booking_id: str, new_status: str):
        return self.booking_service.update_status(
            booking_id,
            new_status,
            repo=self.place_repo
        )
    
    def update_booking_payment(self, booking_id: str, payment_id: str, new_status: str):
        return self.booking_service.update_booking_payment(
            booking_id,
            payment_id,
            new_status,
            repo=self.booking_repo
        )
    
    def is_place_available(self, place_id: str, check_in: str, check_out: str):

        return self.booking_service.is_place_available(
            place_id,
            check_in,
            check_out,
            repo=self.place_repo
        )

    """ payment methods """
    def create_payment(self, payment: dict):

        return self.payment_service.create_payment(
            payment,
            repo=self.payment_repo,
            booking_repo=self.booking_repo
        )
    
    def get_payment_info(self, payment_id: str) -> dict:

        return self.payment_service.get_payment_info(
            payment_id,
            repo=self.payment_repo
        )
    
    def update_payment_status(self, payment_id: str, status: str) -> bool:

        pass

    def delete_payment(self, payment_id: str) -> bool:

        pass

    
    """refund methods"""
    def create_refund(self, refund_data: dict):

        return self.refund_service.create_refund(
            refund_data,
            repo=self.refund_repo,
            payment_repo=self.payment_repo
        )
    
    def update_refund(self, refund_id: str, status: str):
        return self.refund_service.update_payment(
            refund_id,
            status,
            repo=self.refund_repo
        )
    
    def get_refund_info(self, refund_id: str) -> dict:
        
        pass

    def delete_refund(self, refund_id: str) -> bool:
        pass

    def get_refund_info_by_payment_id(self, payment_id: str) -> dict:
        pass

    """ PlaceAmenity Methods """
    def add_amenity_to_place(self, place_id: str, amenity_id: str):

        return self.place_amenity_service.add_amenity_to_place(
            place_id,
            amenity_id,
            repo=self.place_amenity_repo
        )
    
    def remove_amenity_from_place(self, place_amenity_id: str):

        return self.place_amenity_service.remove_amenity_from_place(
            place_amenity_id,
            repo=self.place_amenity_repo
        )
    def get_place_amenity_info(self, place_amenity_id: str) -> dict:

        return self.place_amenity_service.get_place_amenity_info(
            place_amenity_id,
            repo=self.place_amenity_repo
        )
    def update_place_amenity_status(self, place_amenity_id: str, status: str) -> bool:

        return self.place_amenity_service.update_place_amenity_status(
            place_amenity_id,
            status,
            repo=self.place_amenity_repo
        )