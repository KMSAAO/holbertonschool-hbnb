from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price_per_night': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'number_rooms': fields.Integer(default=1),
    'number_bathrooms': fields.Integer(default=1),
    'max_guest': fields.Integer(default=1),
    'owner_id': fields.String(required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    def post(self):
        try:
            new_place = facade.create_place(api.payload)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'price_per_night': new_place.price_per_night
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'price_per_night': p.price_per_night
            } for p in places
        ], 200
