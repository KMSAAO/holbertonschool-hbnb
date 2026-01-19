from app.models.refund import Refund
from app.enums.refund_status import RefundStatus
from app.enums.payment_type import MethodPayment

class RefundServices():

    def create_refund(self, refund_data: dict, repo, payment_repo):

        payment_id = refund_data.get("payment_id")
        if not payment_id or not isinstance(payment_id, str):
            raise ValueError("payment_id is required and must be a string")


        amount_refund = refund_data.get("amount_refund")
        if amount_refund is None or not isinstance(amount_refund, (int, float)) or amount_refund <= 0:
            raise ValueError("amount_refund must be a positive number")

        raw_method = refund_data.get('method_payment')
        try:
            method_payment = raw_method if isinstance(raw_method, MethodPayment) else MethodPayment(raw_method)
        except Exception:
            raise ValueError("Invalid method_payment")

        raw_status = refund_data.get('status')
        try:
            status_refund = raw_status if isinstance(raw_status, RefundStatus) else RefundStatus(raw_status)
        except Exception:
            raise ValueError("Invalid refund status")

        payment = payment_repo.get(payment_id)
        if not payment:
            raise ValueError("Payment not found")

        new_refund = Refund(
            payment_id=payment_id,
            payment=payment,
            amount_refund=amount_refund,
            method_payment=method_payment,
            status=status_refund
        )
        repo.add(new_refund)
        return new_refund

    

    def update_payment(self, refund_id: str, status: str, repo):
        refund = repo.get(refund_id)
        if not refund:
            raise ValueError("Refund not found")

        if isinstance(status, RefundStatus):
            status_refund = status
        else:
            try:
                status_refund = RefundStatus(status)
            except Exception:
                raise ValueError("Invalid status refund")

        refund.status = status_refund
        return repo.save()
    
    def get_refund_info(self, refund_id: str, repo) -> dict:
        refund = repo.get(refund_id)
        if not refund:
            raise ValueError("Refund not found")
        return {
            "id": refund.id,
            "payment_id": refund.payment_id,
            "amount_refund": refund.amount_refund,
            "method_payment": refund.method_payment,
            "status": refund.status.value
        }
    
    def delete_refund(self, refund_id: str, repo) -> bool:
        pass


    def get_refund_by_payment_id(self, payment_id: str, repo):
        pass