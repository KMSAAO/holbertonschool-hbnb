from app.models.payment import Payment
from app.enums.payment_status import PaymentStatus
from app.enums.payment_type import MethodPayment


class PaymentService():

    def create_payment(self, payment: dict, repo, booking_repo) -> Payment:
        booking_id = payment.get('book_id')
        if not booking_id:
            raise ValueError("booking_id is required")

        booking = booking_repo.get(booking_id)
        if not booking:
            raise ValueError("Invalid booking ID")

        amount = payment.get('amount')  # لا حاجة لفحص النوع، الـ Model مسؤول

        raw_method = payment.get('method_payment')
        try:
            method = raw_method if isinstance(raw_method, MethodPayment) else MethodPayment(raw_method)
        except Exception:
            raise ValueError("Invalid method payment")

        raw_status = payment.get('status')
        try:
            status = raw_status if isinstance(raw_status, PaymentStatus) else PaymentStatus(raw_status)
        except Exception:
            raise ValueError("Invalid payment status")

        new_payment = Payment(
            book_id=booking.id,
            booking=booking,
            amount=amount,
            method_payment=method,
            status=status
        )

        repo.add(new_payment)
        return new_payment

    def get_payment_info(self, payment_id: str, repo) -> dict:
        payment = repo.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        return payment.to_dict()

    def update_payment_status(self, payment_id: str, status: str, repo) -> bool:
        payment = repo.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        try:
            new_status = status if isinstance(status, PaymentStatus) else PaymentStatus(status)
        except Exception:
            raise ValueError("Invalid payment status")

        payment.status = new_status
        repo.update(payment)
        return True

    def delete_payment(self, payment_id: str, repo) -> bool:
        payment = repo.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        repo.delete(payment)
        return True

    def get_all_payments(self, repo):
        all_payments = repo.get_all()
        if not all_payments:
            return None

        return all_payments