from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

place_create_model = api.model('PlaceCreate', {
    'title':       fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price':       fields.Float(required=True, description='Price of the place'),
    'status':      fields.String(required=False, description='Status of the place'),
    'latitude':    fields.Float(required=True, description='Latitude'),
    'longitude':   fields.Float(required=True, description='Longitude'),
})

place_response_model = api.model('PlaceResponse', {
    'id':          fields.String,
    'owner_id':    fields.String,
    'title':       fields.String,
    'description': fields.String,
    'price':       fields.Float,
    'status':      fields.String,
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

place_update_model = api.model('PlaceUpdate', {
    'title':       fields.String(required=False),
    'description': fields.String(required=False),
    'price':       fields.Float(required=False),
    'status':      fields.String(required=False),
    'latitude':    fields.Float(required=False),
    'longitude':   fields.Float(required=False),
})


@api.route('/')
class PlaceList(Resource):

    @api.marshal_list_with(place_summary_model, code=200)
    def get(self):
        places = facade.get_all_places()

        if places and hasattr(places[0], 'to_dict'):
            return [
                {
                    "id": p.id,
                    "title": p.title,
                    "latitude": p.latitude,
                    "longitude": p.longitude
                } for p in places
            ], 200

        return places, 200

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    @api.response(400, 'Validation / business error')
    def post(self):
        claims = get_jwt() or {}
        user_id = claims.get("id")
        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        data = api.payload or {}
        data["owner_id"] = str(user_id)

        try:
            place = facade.create_place(place_data=data)
        except ValueError as e:
            api.abort(400, str(e))

        return place, 201


@api.route('/<string:place_id>')
@api.response(404, 'Place not found')
class PlaceDetail(Resource):

    @api.marshal_with(place_response_model, code=200)
    def get(self, place_id):
        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError as e:
            api.abort(404, str(e))
        return place, 200

    @jwt_required()
    @api.expect(place_update_model, validate=False)
    @api.marshal_with(place_response_model, code=200)
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Validation / business error')
    def put(self, place_id):
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)
        user_id = claims.get("id")
        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = place.get("owner_id") if isinstance(place, dict) else getattr(place, "owner_id", None)
        if not is_admin and str(owner_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        data = api.payload or {}

        try:
            updated = facade.update_place(place_id=place_id, place_data=data)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not updated:
            api.abort(404, "Place not found")

        return facade.get_place_info(place_id=place_id), 200

    @jwt_required()
    @api.response(204, 'Place deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Delete error')
    def delete(self, place_id):
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)
        user_id = claims.get("id")
        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = place.get("owner_id") if isinstance(place, dict) else getattr(place, "owner_id", None)
        if not is_admin and str(owner_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        try:
            deleted = facade.delete_place(place_id=place_id)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not deleted:
            api.abort(404, "Place not found")

        return '', 204
