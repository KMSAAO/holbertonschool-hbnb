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

place_update_model = api.model('PlaceUpdate', {
    'title':       fields.String(required=False),
    'description': fields.String(required=False),
    'price':       fields.Float(required=False),
    'status':      fields.String(required=False),
    'latitude':    fields.Float(required=False),
    'longitude':   fields.Float(required=False),
    'owner_id':    fields.String(required=False),
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

def _get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

@api.route('/')
class PlaceList(Resource):

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    @api.response(400, 'Validation / business error')
    def post(self):
        """Create a new place (authenticated user)"""
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

    @api.marshal_list_with(place_summary_model, code=200)
    def get(self):
        """Retrieve list of places (summary)"""
        try:
            places = facade.get_all_places()
            if not places:
                return [], 200

            # إذا يرجع objects
            if hasattr(places[0], 'to_dict'):
                return [
                    {
                        "id": p.id,
                        "title": p.title,
                        "latitude": p.latitude,
                        "longitude": p.longitude
                    } for p in places
                ], 200

            return places, 200
        except Exception as e:
            api.abort(500, str(e))


@api.route('/<string:place_id>')
@api.response(404, 'Place not found')
class PlaceDetail(Resource):

    @api.marshal_with(place_response_model, code=200)
    def get(self, place_id):
        """Get place info by ID"""
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
        """Update place by ID (owner only, admin bypass)"""
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)
        user_id = claims.get("id")

        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = _get_attr(place, "owner_id")

        if not is_admin and str(owner_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        data = api.payload or {}

        if "owner_id" in data and not is_admin:
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

        # رجعي آخر نسخة
        try:
            place = facade.get_place_info(place_id=place_id)
            return place, 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.response(204, 'Place deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Delete error')
    def delete(self, place_id):
        """Delete place by ID (owner only, admin bypass)"""
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)
        user_id = claims.get("id")

        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = _get_attr(place, "owner_id")

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
