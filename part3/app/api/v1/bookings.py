from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.enums.booking_status import BookingStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.auth import get_current_user

api = Namespace('bookings', description='Booking operations')



booking_create_model = api.model('BookingCreate', {
    'check_in':   fields.String(required=True, description="YYYY-MM-DD"),
    'check_out':  fields.String(required=True, description="YYYY-MM-DD"),
})


booking_response_model = api.model('BookingResponse', {
    'id':         fields.String,
    'guest_id':   fields.String,
    'place_id':   fields.String,
    'check_in':   fields.String,
    'check_out':  fields.String,
    'status':     fields.String(enum=[e.value for e in BookingStatus]),
    'created_at': fields.String,
    'updated_at': fields.String,
})


@api.route("/")
class BookingList(Resource):

    @api.expect(booking_create_model, validate=True)
    @api.marshal_with(booking_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new booking"""
        data = api.payload
        current_user = get_current_user()

        try:
            booking = facade.create_booking(data, current_user)
            return booking, 201
        except ValueError as e:
            api.abort(400, str(e))
        except PermissionError as e:
            api.abort(403, str(e))


@api.route('/guest/<string:guest_id>')
@api.response(404, 'Bookings not found for this guest')
class BookingByGuest(Resource):

    @api.marshal_list_with(booking_response_model, code=200)
    @jwt_required()
    def get(self, guest_id: str):
        """Get bookings by guest ID"""
        current_user = get_current_user()
        try:
            bookings = facade.get_bookings_by_guest_id(guest_id, current_user)
            return bookings, 200
        except ValueError as e:
            api.abort(404, str(e))
        except PermissionError as e:
            api.abort(403, str(e))

@api.route('/<string:booking_id>')
@api.response(404, 'Booking not found')
class GetBookingById(Resource):

    @jwt_required()
    @api.marshal_with(booking_response_model, code=200)
    def get(self, booking_id: str):
        user_id = get_jwt_identity()

        try:
            booking = facade.get_booking_by_id(booking_id, user_id)
            return booking, 200
        except ValueError as e:
            api.abort(404, str(e))
        except PermissionError as e:
            api.abort(403, str(e))


@api.route('/my')
class GetMyBookings(Resource):

    @jwt_required()
    @api.marshal_list_with(booking_response_model, code=200)
    def get(self):
        """Get my bookings (from JWT)"""
        user_id = get_jwt_identity()

        try:
            bookings = facade.get_all_bookings(user_id)
            return bookings, 200
        except PermissionError as e:
            api.abort(403, str(e))
        except ValueError as e:
            api.abort(400, str(e))
