from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.enums.payment_status import PaymentStatus
from app.enums.payment_type import MethodPayment
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.auth import get_current_user

api = Namespace('payments', description='Payments related operations')

payment_create_model = api.model('Payment', {
    'booking_id': fields.String(required=True, description='The ID of the associated booking'),
    'amount': fields.Float(required=True, description='The amount of the payment'),
    'method_payment': fields.String(required=True, description='The method of payment', enum=[method.value for method in MethodPayment]),
    'status': fields.String(required=True, description='The status of the payment', enum=[status.value for status in PaymentStatus])
})

payment_response_model = api.model('PaymentResponse', {
    'id': fields.String,
    'booking_id': fields.String,
    'amount': fields.Float,
    'method_payment': fields.String(enum=[method.value for method in MethodPayment]),
    'status': fields.String(enum=[status.value for status in PaymentStatus]),
    'created_at': fields.String,
    'updated_at': fields.String
})


@api.route('/')
class PaymentList(Resource):
    @api.expect(payment_create_model, validate=True)
    @api.marshal_with(payment_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new payment"""
        data = api.payload
        current_user = get_current_user()

        try:
            payment = facade.create_payment(data, current_user)
            return payment, 201
        except ValueError as e:
            api.abort(400, str(e))
        except PermissionError as e:
            api.abort(403, str(e))

@api.route('/<string:payment_id>')
class PaymentResource(Resource):
    @api.marshal_with(payment_response_model)
    @jwt_required()
    def get(self, payment_id):
        """Get a payment by its ID"""
        current_user = get_current_user()

        try:
            payment = facade.get_payment_by_payment_id(payment_id, current_user)
            return payment
        except ValueError as e:
            api.abort(404, str(e))
        except PermissionError as e:
            api.abort(403, str(e))
@api.route('/booking/<string:booking_id>')
class PaymentByBookingResource(Resource):
    @api.marshal_with(payment_response_model)
    @jwt_required()
    def get(self, booking_id):
        """Get a payment by its associated booking ID"""
        current_user = get_current_user()

        try:
            payment = facade.get_payment_by_booking_id(booking_id, current_user)
            return payment
        except ValueError as e:
            api.abort(404, str(e))
        except PermissionError as e:
            api.abort(403, str(e))
