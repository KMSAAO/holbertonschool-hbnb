from app.models.payment import Payment
from app.enums.refund_status import RefundStatus
from app.enums.payment_type import MethodPayment


class PaymentServices():

    def create_payment(self, payment_data: dict, repo, current_user):

        if not current_user:
            raise PermissionError("Authentication required")

        book_id = payment_data.get("book_id")
        if not book_id or not isinstance(book_id, str):
            raise ValueError("book_id is required and must be a string")

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
            status_payment = raw_status if isinstance(raw_status, RefundStatus) else RefundStatus(raw_status)
        except Exception:
            raise ValueError("Invalid payment status")

        new_payment = Payment(
            book_id=book_id,
            amount=amount,
            method_payment=method_payment,
            status=status_payment
        )
        repo.add(new_payment)
        return new_payment
    
    def get_payment_by_payment_id(self, payment_id, repo):
        payment = repo.get_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        return payment
    
    def get_payment_by_booking_id(self, booking_id, repo):
        payment = repo.get_payment_by_booking_id(booking_id)
        if not payment:
            raise ValueError("Payment not found for the given booking_id")
        return payment
    
    def get_payments_by_booking_id(self, booking_id, repo):
        payments = repo.get_payments_by_booking_id(booking_id)
        if not payments:
            raise ValueError("No payments found for the given booking_id")
        return payments
    
    def get_all_payments(self, repo):
        return repo.get_all_payments()
    
    def update_payment_status(self, payment_id, new_status, repo):
        if not isinstance(new_status, RefundStatus):
            raise ValueError("Invalid payment status")
        return repo.update_payment_status(payment_id, new_status)
    