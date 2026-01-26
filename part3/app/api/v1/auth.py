from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import app.services.facade as facade
from flask import jsonify


api = Namespace('auth',  description='Authentication operations')


login_model = api.model('UserLogin', {
    'email': fields.String(required=True, description='User Email'),
    'password': fields.String(required=True, description='User Password'),
})

login_response_model = api.model('UserLoginResponse', {
    'access_token': fields.String
})

Auth_model = api.model('JWT', {
    'Authorization': fields.String(requried=True, description='JWT')
})

Auth_response_model = api.model('AuthResponse', {
    'message': fields.String
})

@api.route('/login')
class AuthLogin(Resource):
    @api.expect(login_model, validate=True)
    @api.marshal_with(login_response_model, code=200)
    @api.response(400, 'Invalid credentials')
    def post(self):
        data = api.payload
        email = data.get('email')
        password = data.get('password')

        try:
            success = facade.login_user(email, password)
            if not success:
                api.abort(400, "Invalid credentials")
            
            user = facade.get_by_attribute('email', email)
            if not user:
                api.abort(400, "User not found")
            else:
                id = user.id
                full_name = user.first_name + " " + user.last_name
                is_admin = user.is_admin
                user_data = {
                    "id": id,
                    "name":full_name,
                    "is_admin": is_admin
                }
                access_token = create_access_token(identity=user_data)
        except ValueError as e:
            api.abort(400, str(e))

        return {'access_token': access_token}, 200
    
@api.route("/protected")
class protected (Resource):
    @api.expect(Auth_model, validate=True)
    @api.marshal_with(Auth_response_model, code=200)
    @api.response(400, 'No user exists with this token')
    @jwt_required()
    def get(self):
        
        current_user = get_jwt_identity()
        if not current_user:
            raise ValueError("No user exists with this token")
        
        return {"message": f"Hello, {current_user}"}, 200