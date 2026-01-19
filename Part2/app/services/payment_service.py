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
        
        amount = payment.get('amount')
        if not amount or not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a non-negative number")

        method_payment = payment.get('method_payment')
        if isinstance(method_payment, MethodPayment):
            method = method_payment
        else:
            try:
                method = MethodPayment(method_payment)
            except Exception:
                raise ValueError("Invalid method payment")
            
        status = payment.get('status')
        if not status:
            raise ValueError("status is required")

        if isinstance(status, PaymentStatus):
            status_payment = status
        else:
            try:
                status_payment = PaymentStatus(status)
            except Exception:
                raise ValueError("Invalid status payment")

        new_payment = Payment(
            book_id=booking.id,
            booking=booking,
            amount=amount,
            method_payment=method,
            status=status_payment
        )

        repo.add(new_payment)
        return new_payment
    
    def get_payment_info(self, payment_id: str, repo) -> dict:
        payment = repo.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        return {
            "id": payment.id,
            "book_id": payment.book_id,
            "amount": payment.amount,
            "method_payment": payment.method_payment.value,
            "status": payment.status.value
        }

    """ this method will implement later """
    def update_payment_status(self, payment_id: str, status: str, repo  ) -> bool:

        pass

    def delete_payment(self, payment_id: str, repo) -> bool:
        payment = repo.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        repo.delete(payment)
        return True
    
    