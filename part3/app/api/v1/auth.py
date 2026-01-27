from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
import app.services.facade as facade

api = Namespace('auth',  description='Authentication operations')

login_model = api.model('UserLogin', {
    'email': fields.String(required=True, description='User Email'),
    'password': fields.String(required=True, description='User Password'),
})

login_response_model = api.model('UserLoginResponse', {
    'access_token': fields.String
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

            user_id = user.id
            full_name = f"{user.first_name} {user.last_name}"
            is_admin = user.is_admin

            access_token = create_access_token(
                identity=str(user_id),
                additional_claims={
                    "id": str(user_id),
                    "name": full_name,
                    "is_admin": bool(is_admin)
                }
            )
        except ValueError as e:
            api.abort(400, str(e))

        return {'access_token': access_token}, 200


@api.route("/protected")
class Protected(Resource):
    @api.marshal_with(Auth_response_model, code=200)
    @jwt_required()
    def get(self):
        claims = get_jwt()
        user_id = get_jwt_identity()

        if claims.get("is_admin", False):
            return {"message": f"Hello, Admin {user_id}"}, 200

        return {"message": f"Hello, user {user_id}"}, 200
