from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
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


def _get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@api.route('/')
class PlaceList(Resource):

    @api.marshal_list_with(place_summary_model, code=200)
    def get(self):
        """Public: list places"""
        try:
            places = facade.get_all_places()
            return places, 200
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    @api.response(400, 'Validation / business error')
    def post(self):
        """Authenticated: create place (owner_id from token)"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Missing/invalid token")

        data = api.payload or {}
        data["owner_id"] = str(current_user_id)

        try:
            place = facade.create_place(place_data=data)
            return place, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:place_id>')
@api.response(404, 'Place not found')
class PlaceDetail(Resource):

    @api.marshal_with(place_response_model, code=200)
    def get(self, place_id):
        """Public: get place by id"""
        try:
            place = facade.get_place_info(place_id=place_id)
            return place, 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(place_update_model, validate=False)
    @api.marshal_with(place_response_model, code=200)
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Validation / business error')
    def put(self, place_id):
        """Authenticated: update place (owner only)"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Missing/invalid token")

        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = _get_attr(place, "owner_id")
        if str(owner_id) != str(current_user_id):
            api.abort(403, "Unauthorized action.")

        data = api.payload or {}
        data.pop("owner_id", None)

        try:
            updated = facade.update_place(place_id=place_id, place_data=data)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not updated:
            api.abort(404, "Place not found")

        try:
            return facade.get_place_info(place_id=place_id), 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.response(204, 'Place deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Delete error')
    def delete(self, place_id):
        """Authenticated: delete place (owner only)"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Missing/invalid token")

        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = _get_attr(place, "owner_id")
        if str(owner_id) != str(current_user_id):
            api.abort(403, "Unauthorized action.")

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
