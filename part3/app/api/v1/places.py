from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace("places", description="Place operations")

place_create_model = api.model("PlaceCreate", {
    "title": fields.String(required=True),
    "description": fields.String(required=False),
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(required=False),
    "description": fields.String(required=False),
    "price": fields.Float(required=False),
    "status": fields.String(required=False),
    "latitude": fields.Float(required=False),
    "longitude": fields.Float(required=False),
})

place_response_model = api.model("PlaceResponse", {
    "id": fields.String,
    "owner_id": fields.String,
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "status": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "created_at": fields.String,
    "updated_at": fields.String,
})


def _get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_response_model, code=200)
    def get(self):
        return facade.get_all_places(), 200

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Invalid token")

        data = api.payload or {}

        data["owner_id"] = str(current_user_id)

        try:
            place = facade.create_place(data)
            return place, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.marshal_with(place_response_model, code=200)
    def get(self, place_id):
        try:
            return facade.get_place_info(place_id), 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(place_update_model, validate=False)
    @api.marshal_with(place_response_model, code=200)
    def put(self, place_id):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Invalid token")

        try:
            place = facade.get_place_info(place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = str(_get_attr(place, "owner_id"))
        if owner_id != str(current_user_id):
            api.abort(403, "Unauthorized action")

        data = api.payload or {}
        data.pop("owner_id", None)

        try:
            updated = facade.update_place(place_id, data)
            if not updated:
                api.abort(400, "Update failed")

            place = facade.get_place_info(place_id)
            return place, 200
        except ValueError as e:
            api.abort(400, str(e))