from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace("users", description="User operations")

# --- Models ---
user_create_model = api.model("UserCreate", {
    "first_name": fields.String(required=True, description="First Name"),
    "last_name":  fields.String(required=True, description="Last Name"),
    "email":      fields.String(required=True, description="Email"),
    "password":   fields.String(required=True, description="Password"),
    "is_admin":   fields.Boolean(required=False, default=False, description="Request Admin Role"),
    "admin_code": fields.String(required=False, description="Admin signup code"),
    "is_active":  fields.Boolean(required=False, default=True, description="Is Active"),
})

user_response_model = api.model("UserResponse", {
    "id":         fields.String,
    "first_name": fields.String,
    "last_name":  fields.String,
    "email":      fields.String,
    "is_admin":   fields.Boolean,
    "is_active":  fields.Boolean,
    "created_at": fields.String,
    "updated_at": fields.String,
})

user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(required=False),
    "last_name":  fields.String(required=False),
    "email":      fields.String(required=False),
    "password":   fields.String(required=False),
})

# --- Routes ---

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_response_model, code=200)
    def get(self):
        """Get all users"""
        return facade.get_all_users(), 200

    # نقلنا دالة الإنشاء (POST) إلى هنا لتصبح في العنوان الرئيسي
    @api.expect(user_create_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Register a new user"""
        data = api.payload or {}
        try:
            # التحقق من وجود الإيميل مسبقاً
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user:
                 api.abort(400, "User with this email already exists")

            user = facade.create_user(data)
            return user, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:user_id>")
class UserDetail(Resource):
    @api.marshal_with(user_response_model, code=200)
    def get(self, user_id):
        """Get user by ID"""
        try:
            return facade.get_user(user_id), 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(user_update_model, validate=False)
    @api.marshal_with(user_response_model, code=200)
    def put(self, user_id):
        """Update user info"""
        current_user_id = get_jwt_identity()

        # السماح فقط لصاحب الحساب بالتعديل
        if not current_user_id or str(current_user_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        data = api.payload or {}
        # منع تعديل الإيميل أو الباسورد من هنا
        if "email" in data or "password" in data:
            api.abort(400, "Cannot modify email or password directly")

        try:
            updated = facade.update_user(user_id, data)
            return updated, 200
        except ValueError as e:
            api.abort(400, str(e))
