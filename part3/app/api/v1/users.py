from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
import app.services.facade as facade

api = Namespace('users', description='User operations')

user_register_model = api.model('UserRegister', {
    'first_name': fields.String(required=True),
    'last_name':  fields.String(required=True),
    'email':      fields.String(required=True),
    'password':   fields.String(required=True),
    'is_admin':   fields.Boolean(required=False, default=False),
    'is_active':  fields.Boolean(required=False, default=True),
})

user_response_model = api.model('UserResponse', {
    'id':         fields.String,
    'first_name': fields.String,
    'last_name':  fields.String,
    'email':      fields.String,
    'is_admin':   fields.Boolean,
    'is_active':  fields.Boolean,
    'created_at': fields.String,
    'updated_at': fields.String,
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False),
    'last_name':  fields.String(required=False),
    'email':      fields.String(required=False),
    'password':   fields.String(required=False),
    'is_admin':   fields.Boolean(required=False),
    'is_active':  fields.Boolean(required=False),
})


@api.route('/register')
class UserRegister(Resource):
    @api.expect(user_register_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        user = facade.register_user(api.payload)
        return user, 201


@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model, code=200)
    def get(self):
        return facade.get_all_users(), 200


@api.route('/<string:user_id>')
class UserDetail(Resource):

    @api.marshal_with(user_response_model, code=200)
    def get(self, user_id):
        user = facade.get_user(user_id)
        return user, 200

    @jwt_required()
    @api.expect(user_update_model, validate=False)
    @api.marshal_with(user_response_model, code=200)
    def put(self, user_id):
        current_user = get_jwt_identity()

        if str(current_user) != str(user_id):
            api.abort(403, "You can only modify your own profile")

        data = api.payload or {}

        if "email" in data or "password" in data or "is_admin" in data:
            api.abort(400, "Email, password and admin flag cannot be changed here")

        facade.update_user(user_id, data)
        updated = facade.get_user(user_id)
        return updated, 200
