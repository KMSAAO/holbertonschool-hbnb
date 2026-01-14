from app.models.refund import Refund
from app.enums.refund_status import RefundStatus

class RefundServices():

    def create_refund(self, refund_data: dict, amount_refund, method_payment, status, repo):

        payment_id = refund_data.get("payment_id")
        if not payment_id or not isinstance(payment_id, str):
            raise ValueError("payment_id is required and must be a string")
        
        amount_refund = refund_data.get("amount_refund")
        if amount_refund is None or not isinstance(amount_refund, (int, float)) or amount_refund < 0:
            raise ValueError("amount_refund must be a non-negative number")
        
        status = refund_data.get('status')
        if isinstance(status, RefundStatus):
            status_refund = status
        else:
            try:
                status = RefundStatus(status)
            except Exception:
                raise ValueError("Invalid status refund")
            
        new_refund = Refund(
            payment_id=payment_id,
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
        repo.save()
        return True
    
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