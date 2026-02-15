from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
import app.services.facade as facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User Email'),
    'password': fields.String(required=True, description='User Password'),
})

# 🔥 التعديل الأول: السماح بمرور البيانات الإضافية في الاستجابة 🔥
login_response_model = api.model('LoginResponse', {
    'access_token': fields.String,
    'id': fields.String,          # ضروري جداً
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'is_admin': fields.Boolean
})

protected_response_model = api.model('ProtectedResponse', {
    'message': fields.String
})


@api.route('/login')
class AuthLogin(Resource):
    @api.expect(login_model, validate=True)
    @api.marshal_with(login_response_model, code=200)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        data = api.payload or {}
        email = data.get('email')
        password = data.get('password')

        try:
            success = facade.login_user(email, password)
            if not success:
                return {"error": "Invalid credentials"}, 401

            user = None
            if hasattr(facade, "get_user_by_email"):
                user = facade.get_user_by_email(email)
            # fallback
            if not user:
                user = facade.get_by_attribute('email', email)

            if not user:
                return {"error": "User not found"}, 401

            user_id = str(user.id)
            full_name = f"{user.first_name} {user.last_name}"
            is_admin = bool(getattr(user, "is_admin", False))

            access_token = create_access_token(
                identity=user_id, 
                additional_claims={
                    "is_admin": is_admin,
                    "id": user_id,
                    "name": full_name
                }
            )

            # 🔥 التعديل الثاني: إرجاع البيانات المطلوبة مع التوكن 🔥
            return {
                'access_token': access_token,
                'id': user_id,            # <--- هذا هو المفتاح المفقود!
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': is_admin
            }, 200

        except ValueError as e:
            api.abort(400, str(e))


@api.route('/protected')
class Protected(Resource):
    @jwt_required()
    @api.marshal_with(protected_response_model, code=200)
    def get(self):
        """Protected endpoint that requires a valid JWT token"""
        claims = get_jwt()
        user_id = get_jwt_identity()

        if claims.get("is_admin", False):
            return {"message": f"Hello, Admin {user_id}"}, 200

        return {"message": f"Hello, user {user_id}"}, 200