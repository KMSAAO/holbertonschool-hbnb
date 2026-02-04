from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token
)
from app.services import facade

api = Namespace("users", description="User operations")

user_register_model = api.model("UserRegister", {
    "first_name": fields.String(required=True),
    "last_name":  fields.String(required=True),
    "email":      fields.String(required=True),
    "password":   fields.String(required=True),
    "is_admin":   fields.Boolean(required=False, default=False),
    "is_active":  fields.Boolean(required=False, default=True),
})

user_login_model = api.model("UserLogin", {
    "email":    fields.String(required=True),
    "password": fields.String(required=True),
})

user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(required=False),
    "last_name":  fields.String(required=False),
    "email":      fields.String(required=False),
    "password":   fields.String(required=False),
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


def _get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@api.route("/register")
class UserRegister(Resource):
    @api.expect(user_register_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        data = api.payload or {}
        try:
            user = facade.register_user(data)
            return user, 201
        except ValueError as e:
            api.abort(400, str(e))


# @api.route("/login")
# class UserLogin(Resource):
#     @api.expect(user_login_model, validate=True)
#     def post(self):
#         data = api.payload or {}
#         email = data.get("email")
#         password = data.get("password")

#         ok = facade.login_user(email=email, password=password)
#         if not ok:
#             api.abort(401, "Invalid credentials")

#         user = facade.get_user_by_email(email)
#         if not user:
#             api.abort(401, "Invalid credentials")

#         uid = str(_get_attr(user, "id"))
#         is_admin = bool(_get_attr(user, "is_admin", False))

#         access_token = create_access_token(
#             identity=uid,
#             additional_claims={"id": uid, "is_admin": is_admin},
#         )
#         return {"access_token": access_token}, 200


@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_response_model, code=200)
    def get(self):
        return facade.get_all_users(), 200


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

        if not current_user_id:
            api.abort(401, "Invalid token")

        if str(current_user_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        data = api.payload or {}

        if "email" in data or "password" in data:
            api.abort(400, "You cannot modify email or password")

        try:
            updated = facade.update_user(user_id, data)
            return updated, 200
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)
