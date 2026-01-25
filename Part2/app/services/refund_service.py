from app.models.refund import Refund
from app.enums.refund_status import RefundStatus
from app.enums.payment_type import MethodPayment


class RefundServices:

    def create_refund(self, refund_data: dict, repo, payment_repo):
        payment_id = refund_data.get("payment_id")
        if not payment_id or not isinstance(payment_id, str):
            raise ValueError("payment_id is required and must be a string")

        amount_refund = refund_data.get("amount_refund")  # التحقق منه يكون داخل الـ model

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

        try:
            status_refund = status if isinstance(status, RefundStatus) else RefundStatus(status)
        except Exception:
            raise ValueError("Invalid refund status")

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
        refund = repo.get(refund_id)
        if not refund:
            raise ValueError("Refund not found")
        repo.delete(refund)
        return True

    def get_refund_by_payment_id(self, payment_id: str, repo):
        return repo.filter_by(payment_id=payment_id)

    def get_all_refunds(self, repo):
        get_all_refunds = repo.list_all()

        if not get_all_refunds:
            return None
        return get_all_refunds