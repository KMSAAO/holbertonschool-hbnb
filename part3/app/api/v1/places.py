from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

place_create_model = api.model('PlaceCreate', {
    'title':       fields.String(required=True),
    'description': fields.String(required=False),
    'price':       fields.Float(required=True),
    'latitude':    fields.Float(required=True),
    'longitude':   fields.Float(required=True),
})

place_update_model = api.model('PlaceUpdate', {
    'title':       fields.String(required=False),
    'description': fields.String(required=False),
    'price':       fields.Float(required=False),
    'latitude':    fields.Float(required=False),
    'longitude':   fields.Float(required=False),
})

place_response_model = api.model('PlaceResponse', {
    'id':          fields.String,
    'owner_id':    fields.String,
    'title':       fields.String,
    'description': fields.String,
    'price':       fields.Float,
    'latitude':    fields.Float,
    'longitude':   fields.Float,
    'created_at':  fields.String,
    'updated_at':  fields.String,
})

place_summary_model = api.model('PlaceSummary', {
    'id':        fields.String,
    'title':     fields.String,
    'latitude':  fields.Float,
    'longitude': fields.Float,
})


@api.route('/')
class PlaceList(Resource):

    @api.marshal_list_with(place_summary_model, code=200)
    def get(self):
        return facade.get_all_places(), 200

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        claims = get_jwt()
        user_id = claims.get("id")

        if not user_id:
            api.abort(401, "Invalid token")

        data = api.payload
        data["owner_id"] = user_id

        try:
            place = facade.create_place(data)
            return place, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:place_id>')
class PlaceDetail(Resource):

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
        claims = get_jwt()
        user_id = claims.get("id")
        is_admin = claims.get("is_admin", False)

        try:
            place = facade.get_place_info(place_id)
        except ValueError:
            api.abort(404, "Place not found")

        owner_id = place["owner_id"]

        if not is_admin and owner_id != user_id:
            api.abort(403, "Unauthorized")

        try:
            facade.update_place(place_id, api.payload)
            return facade.get_place_info(place_id), 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    def delete(self, place_id):
        claims = get_jwt()
        user_id = claims.get("id")
        is_admin = claims.get("is_admin", False)

        try:
            place = facade.get_place_info(place_id)
        except ValueError:
            api.abort(404, "Place not found")

        owner_id = place["owner_id"]

        if not is_admin and owner_id != user_id:
            api.abort(403, "Unauthorized")

        try:
            facade.delete_place(place_id)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))
