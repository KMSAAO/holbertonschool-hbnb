from flask_restx import Namespace, Resource, fields
# أضفنا get_jwt هنا لكي يعمل شرط التحقق من الأدمن
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt 
from app.services import facade

api = Namespace("users", description="User operations")

# --- النماذج (Models) تبقى كما هي بدون تغيير ---
user_create_model = api.model("UserCreate", {
    "first_name": fields.String(required=True),
    "last_name":  fields.String(required=True),
    "email":      fields.String(required=True),
    "password":   fields.String(required=True),
    "is_admin":   fields.Boolean(required=False, default=False),
    "admin_code": fields.String(required=False),
    "is_active":  fields.Boolean(required=False, default=True),
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

# --- المسارات (Routes) ---

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_response_model, code=200)
    def get(self):
        return facade.get_all_users(), 200

    @api.expect(user_create_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        data = api.payload or {}
        try:
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
        try:
            return facade.get_user(user_id), 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(user_update_model, validate=False)
    @api.marshal_with(user_response_model, code=200)
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        if not current_user_id or str(current_user_id) != str(user_id):
            api.abort(403, "Unauthorized action")
        data = api.payload or {}
        if "email" in data or "password" in data:
            api.abort(400, "Cannot modify email or password directly")
        try:
            updated = facade.update_user(user_id, data)
            return updated, 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    def delete(self, user_id):
        """حذف المستخدم (يتطلب صلاحية أدمن)"""
        # جلب الـ claims للتأكد من حالة الأدمن
        claims = get_jwt() 
        
        # التحقق من الصلاحية
        if not claims.get("is_admin"):
            api.abort(403, "Admin privileges required")
        
        try:
            # تنفيذ الحذف عبر الـ facade
            success = facade.delete_user(user_id)
            if success:
                return {"message": "User deleted successfully"}, 200
            else:
                api.abort(404, "User not found")
        except ValueError as e:
            api.abort(400, str(e))