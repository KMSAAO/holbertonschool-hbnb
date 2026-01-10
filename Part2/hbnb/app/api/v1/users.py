# app/api/v1/users.py

from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# ===== Swagger Models =====

user_register_model = api.model('UserRegister', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name':  fields.String(required=True, description='Last name'),
    'email':      fields.String(required=True, description='Email'),
    'password':   fields.String(required=True, description='Password'),
    'is_admin':   fields.Boolean(required=False, description='Is admin', default=False),
})

login_model = api.model('UserLogin', {
    'email':    fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
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


# ===== /api/v1/users/register =====

@api.route('/register')
class UserRegister(Resource):
    @api.expect(user_register_model, validate=True)
    @api.response(201, 'User created', user_response_model)
    @api.response(400, 'Validation error')
    def post(self):
        """Register new user"""
        data = api.payload

        try:
            user = facade.register_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400


# ===== /api/v1/users/login =====

@api.route('/login')
class UserLogin(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(400, 'Invalid credentials')
    def post(self):
        """Login user"""
        data = api.payload
        email = data.get('email')
        password = data.get('password')

        try:
            success = facade.login_user(email, password)
            if success:
                return {'message': 'Login successful'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400


# ===== /api/v1/users/<user_id> =====

@api.route('/<string:user_id>')
@api.response(404, 'User not found')
class UserDetail(Resource):

    @api.response(200, 'Success', user_response_model)
    def get(self, user_id):
        """Get user info by ID"""
        try:
            user_dict = facade.get_user(user_id)
            return {
        "id": str(user.id),          # لو id عندك UUID حوّله سترنق
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
        }, 201
        except ValueError as e:
            return {'message': str(e)}, 404

    @api.expect(user_register_model, validate=False)
    @api.response(200, 'User updated', user_response_model)
    @api.response(400, 'Validation error')
    def put(self, user_id):
        """Update user by ID"""
        data = api.payload or {}

        try:
            updated = facade.update_user(user_id, data)
            if not updated:
                return {'message': 'User not found'}, 404

            user_dict = facade.get_user(user_id)
            return user_dict, 200
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                return {'message': msg}, 404
            return {'message': msg}, 400

    @api.response(204, 'User deleted')
    def delete(self, user_id):
        """Delete user by ID"""
        try:
            deleted = facade.delete_user(user_id)
            if not deleted:
                return {'message': 'User not found'}, 404
            return '', 204
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                return {'message': msg}, 404
            return {'message': msg}, 400
