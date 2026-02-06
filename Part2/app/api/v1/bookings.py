from flask_restx import Namespace, Resource, fields
import app.services.facade as facade
from app.enums.booking_status import BookingStatus  

api = Namespace('bookings', description='Booking operations')

booking_create_model = api.model('BookingCreate', {
    'guest_id':   fields.String(required=True, description='Guest ID'),
    'place_id':   fields.String(required=True, description='Place ID'),
    'check_in':   fields.String(required=True, description='Check-in datetime in ISO format'),
    'check_out':  fields.String(required=True, description='Check-out datetime in ISO format'),
    'status':     fields.String(required=True, description='Booking status', enum=BookingStatus),
})

booking_update_model = api.model('BookingUpdate', {
    'guest_id':   fields.String(required=False),
    'place_id':   fields.String(required=False),
    'check_in':   fields.String(required=False),
    'check_out':  fields.String(required=False),
    'status':     fields.String(required=False, enum=BookingStatus),
})

booking_response_model = api.model('BookingResponse', {
    'id':         fields.String,
    'guest_id':   fields.String,
    'place_id':   fields.String,
    'check_in':   fields.String,
    'check_out':  fields.String,
    'status':     fields.String(enum=BookingStatus),
    'created_at': fields.String,
    'updated_at': fields.String,
})

@api.route('/')
class BookingList(Resource):
    @api.expect(booking_create_model, validate=True)
    @api.marshal_with(booking_response_model, code=201)
    def post(self):
        """Create a new booking"""
        data = api.payload
        try:
            booking = facade.create_booking(data)
        except ValueError as e:
            api.abort(400, str(e))
        return booking, 201

    @api.marshal_list_with(booking_response_model, code=200)
    def get(self):
        """Get all bookings"""
        return facade.get_all_bookings(), 200


@api.route('/<string:booking_id>')
@api.response(404, 'Booking not found')
class BookingDetail(Resource):
    @api.marshal_with(booking_response_model, code=200)
    def get(self, booking_id):
        """Get booking by ID"""
        try:
            booking = facade.get_booking(booking_id)
        except ValueError as e:
            api.abort(404, str(e))
        return booking, 200

    @api.expect(booking_update_model, validate=False)
    @api.marshal_with(booking_response_model, code=200)
    def put(self, booking_id):
        """Update booking by ID"""
        data = api.payload or {}
        try:
            updated = facade.update_booking(booking_id, data)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if isinstance(updated, dict):
            return updated, 200

        if not updated:
            api.abort(404, "Booking not found")

        booking = facade.get_booking(booking_id)
        return booking, 200

    @api.response(204, 'Booking deleted')
    def delete(self, booking_id):
        """Delete booking by ID"""
        try:
            deleted = facade.delete_booking(booking_id)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not deleted:
            api.abort(404, "Booking not found")

        return '', 204
