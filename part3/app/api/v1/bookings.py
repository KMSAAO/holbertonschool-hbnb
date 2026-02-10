from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.enums.booking_status import BookingStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.auth import get_current_user

api = Namespace('bookings', description='Booking operations')



booking_create_model = api.model('BookingCreate', {
    'check_in':   fields.String(required=True, description="YYYY-MM-DD"),
    'check_out':  fields.String(required=True, description="YYYY-MM-DD"),
    'status':     fields.String(
        required=True,
        enum=[e.value for e in BookingStatus]
    ),
})

booking_update_model = api.model('BookingUpdate', {
    'place_id':   fields.String(required=False),
    'check_in':   fields.String(required=False),
    'check_out':  fields.String(required=False),
    'status':     fields.String(enum=[e.value for e in BookingStatus]),
})

booking_get_guest_by_id_model = api.model('BookingGetGuestById', {
    'guest_id': fields.String(required=True),
})

booking_update_status_model = api.model('BookingUpdateStatus', {
    'status': fields.String(enum=[e.value for e in BookingStatus]),
})

booking_update_response_model = api.model('BookingUpdateResponse', {
    'status': fields.String(enum=[e.value for e in BookingStatus]),
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

    @api.marshal_list_with(booking_get_guest_by_id_model, code=200)
    def get(self, guest_id: str):
        """Get bookings by guest ID"""
        try:
            bookings = facade.get_bookings_by_guest_id(guest_id)
            return bookings, 200
        except ValueError as e:
            api.abort(404, str(e))
        except PermissionError as e:
            api.abort(403, str(e))


@api.route('/<string:booking_id>/status')
@api.response(404, 'Booking not found')
class BookingStatusUpdate(Resource):

    @api.expect(booking_update_status_model, validate=True)
    @api.marshal_with(booking_update_response_model, code=200)
    def put(self, booking_id: str):
        """Update booking status by ID"""
        data = api.payload
        status = facade.update_booking_status(booking_id, data.get("status"))
        return {"status": status}, 200


@api.route('/<string:booking_id>')
@api.response(404, 'Booking not found')
class GetBookingById(Resource):

    @jwt_required()
    @api.marshal_with(booking_response_model, code=200)
    def get(self, booking_id: str):
        user_id = get_jwt_identity()

        try:
            booking = facade.get_bookings_by_id(booking_id, user_id)
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


@api.route('/<string:booking_id>')
class BookingUpdate(Resource):

    @api.expect(booking_update_model, validate=False)
    @api.marshal_with(booking_response_model, code=200)
    def put(self, booking_id: str):
        """Update booking by ID"""
        data = api.payload or {}

        try:
            updated = (
                facade.update_booking_status(booking_id, data.get("status"))
                if "status" in data
                else facade.update_booking_dates(booking_id, data)
            )
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not updated:
            api.abort(404, "Booking not found")

        booking = facade.get_bookings_by_id(booking_id)
        return booking, 200
