from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
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
                access_token = create_access_token(
                    identity=str(id),
                    additional_claims={"name": f"{full_name}", "is_amdin": is_admin}
                )
        except ValueError as e:
            api.abort(400, str(e))

        return {'access_token': access_token}, 200
    
@api.route("/protected")
class protected (Resource):
    @api.marshal_list_with(Auth_response_model, code=200)
    @jwt_required()
    def get(self):
        
        id_user = get_jwt_identity()

        user = facade.get_user(id_user)
        if not id_user:
            raise ValueError("No user exists with this token")
        
        admin = user['is_admin']

        if admin is True:
            return {"message": f"Hello, Admin {id_user}"}, 200
        elif admin is False:
            return {"message": f"Hello, user {id_user}"}, 200
        