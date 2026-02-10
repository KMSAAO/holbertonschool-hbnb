from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import create_access_token, jwt_required
from app.api.v1.auth import get_current_user

api = Namespace('guests', description='Guest operations')

guest_register_model = api.model('GuestRegister', {
    'first_name': fields.String(required=True),
    'last_name':  fields.String(required=True),
    'email':      fields.String(required=True),
    'password':   fields.String(required=True),
    'bio':        fields.String(required=False)
})

guest_response_model = api.model('GuestResponse', {
    'id':           fields.String,
    'user_id':      fields.String,
    'bio':          fields.String,
    'created_date': fields.String,
    'updated_at':   fields.String
})

@api.route('/register')
class GuestRegister(Resource):
    @api.expect(guest_register_model, validate=True)
    @api.response(201, 'Guest registered successfully')
    @api.response(400, 'Validation error')
    def post(self):
        """Register user and create guest"""
        data = api.payload
    
        try:
            user_data = {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "email": data["email"],
                "password": data["password"]
            }
            user = facade.create_user(user_data)

            guest_data = {
                "user_id": user.id,
                "bio": data.get("bio", "")
            }

            guest = facade.register_as_guest(guest_data)

            access_token = create_access_token(
                identity=user.id,
                additional_claims={"role": "guest"}
            )

            response = guest.to_dict()
            response['access_token'] = access_token

        except ValueError as e:
            api.abort(400, str(e))

        return response, 201

@api.route('/<string:user_id>')
class GuestInfo(Resource):
    @api.response(200, 'Success', guest_response_model)
    @api.response(404, 'Guest not found')
    @jwt_required()
    def get(self, user_id):
        """Get guest info by user_id"""
        current_user = get_current_user()
        try:
            guest = facade.get_guest_by_user_id(user_id, current_user)
            if not guest:
                api.abort(404, "Guest not found")
            return guest.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))
    
@api.route('/')
class GuestList(Resource):
    @api.response(200, 'Success', [guest_response_model])
    @api.response(403, 'Forbidden')
    @jwt_required()
    def get(self):
        """Get all guests"""
        current_user = get_current_user()

        try:
            guests = facade.get_all_guests(current_user)
            return [guest.to_dict() for guest in guests], 200

        except PermissionError as e:
            api.abort(403, str(e))