from app.models.payment import Payment
from app.enums.payment_status import PaymentStatus
from app.enums.payment_type import MethodPayment


class PaymentServices():

    def create_payment(self, payment_data: dict, repo, current_user):

        if not current_user:
            raise PermissionError("Authentication required")

        booking_id = payment_data.get("booking_id")
        if not booking_id or not isinstance(booking_id, str):
            raise ValueError("booking_id is required and must be a string")

        amount = payment_data.get("amount")
        if not amount or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("amount is required and must be a positive number")

        raw_method = payment_data.get('method_payment')
        try:
            method_payment = raw_method if isinstance(raw_method, MethodPayment) else MethodPayment(raw_method)
        except Exception:
            raise ValueError("Invalid method_payment")

        raw_status = payment_data.get('status')
        try:
            status_payment = raw_status if isinstance(raw_status, PaymentStatus) else PaymentStatus(raw_status)
        except Exception:
            raise ValueError("Invalid payment status")

        new_payment = Payment(
            booking_id=booking_id,
            amount=amount,
            method_payment=method_payment,
            status=status_payment
        )
        repo.add(new_payment)
        return new_payment
    
    def get_payment_by_payment_id(self, payment_id, repo, current_user):
        if not current_user:
            raise PermissionError("Authentication required")
        payment = repo.get_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        return payment
    
    def get_payment_by_booking_id(self, booking_id, repo, current_user):
        if not current_user:
            raise PermissionError("Authentication required")
        payment = repo.get_payment_by_booking_id(booking_id)
        if not payment:
            raise ValueError("Payment not found for the given booking_id")
        return payment
    
    def get_all_payments(self, repo, current_user):
        if not current_user:
            raise PermissionError("Authentication required")
        return repo.get_all_payments()
    
    def update_payment_status(self, payment_id, new_status, repo):
        if not isinstance(new_status, PaymentStatus):
            raise ValueError("Invalid payment status")
        return repo.update_payment_status(payment_id, new_status)
    