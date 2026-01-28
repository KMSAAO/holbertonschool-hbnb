from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
import app.services.facade as facade

api = Namespace('users', description='User operations')

user_register_model = api.model('UserRegister', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name':  fields.String(required=True, description='Last name'),
    'email':      fields.String(required=True, description='Email'),
    'password':   fields.String(required=True, description='Password'),
    'is_admin':   fields.Boolean(required=False, description='Is admin', default=False),
    'is_active':  fields.Boolean(required=False, description='Is active', default=True),
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
    'first_name': fields.String(required=False, description='First name'),
    'last_name':  fields.String(required=False, description='Last name'),
    'email':      fields.String(required=False, description='Email'),
    'password':   fields.String(required=False, description='Password'),
    'is_admin':   fields.Boolean(required=False, description='Is admin'),
    'is_active':  fields.Boolean(required=False, description='Is active'),
})


@api.route('/register')
class UserRegister(Resource):
    @api.expect(user_register_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(400, 'Validation error')
    def post(self):
        data = api.payload
        try:
            user = facade.register_user(data)
        except ValueError as e:
            api.abort(400, str(e))
        return user, 201


@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model, code=200)
    def get(self):
        users = facade.get_all_users()
        return users, 200

    @jwt_required()
    @api.expect(user_register_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Validation error')
    def post(self):
        claims = get_jwt() or {}
        if not claims.get("is_admin", False):
            api.abort(403, "Admin privileges required")

        data = api.payload or {}
        email = data.get("email")
        if not email:
            api.abort(400, "Email is required")

        existing = facade.get_by_attribute("email", email)
        if existing:
            api.abort(400, "Email already registered")

        try:
            user = facade.register_user(data)
        except ValueError as e:
            api.abort(400, str(e))

        return user, 201


@api.route('/<string:user_id>')
@api.response(404, 'User not found')
class UserDetail(Resource):

    @api.marshal_with(user_response_model, code=200)
    def get(self, user_id):
        try:
            user = facade.get_user(user_id)
        except ValueError as e:
            api.abort(404, str(e))
        return user, 200

    @jwt_required()
    @api.expect(user_update_model, validate=False)
    @api.marshal_with(user_response_model, code=200)
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Validation error')
    def put(self, user_id):
        claims = get_jwt() or {}
        if not claims.get("is_admin", False):
            api.abort(403, "Admin privileges required")

        data = api.payload or {}

        email = data.get("email")
        if email:
            existing = facade.get_by_attribute("email", email)
            if existing and str(existing.id) != str(user_id):
                api.abort(400, "Email already in use")

        try:
            updated = facade.update_user(user_id, data)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if isinstance(updated, dict):
            return updated, 200

        if not updated:
            api.abort(404, "User not found")

        user = facade.get_user(user_id)
        return user, 200

    @jwt_required()
    @api.response(204, 'User deleted')
    @api.response(403, 'Admin privileges required')
    @api.response(400, 'Delete error')
    def delete(self, user_id):
        claims = get_jwt() or {}
        if not claims.get("is_admin", False):
            api.abort(403, "Admin privileges required")

        try:
            deleted = facade.delete_user(user_id)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not deleted:
            api.abort(404, "User not found")

        return '', 204
