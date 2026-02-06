from flask_restx import Namespace, Resource, fields
from app.services import facade

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

        except ValueError as e:
            api.abort(400, str(e))

        return {
            "message": "Guest registered successfully",
            "guest": guest
        }, 201
