from flask_restx import Namespace, Resource, fields

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price_per_night': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'number_rooms': fields.Integer(default=1, description='Number of rooms'),
    'number_bathrooms': fields.Integer(default=1, description='Number of bathrooms'),
    'max_guest': fields.Integer(default=1, description='Maximum number of guests'),
    'owner_id': fields.String(required=True, description='ID of the owner (User)')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        try:
            new_place = facade.create_place(api.payload)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'price_per_night': new_place.price_per_night
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved')
    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'latitude': p.latitude,
                'longitude': p.longitude
            } for p in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price_per_night': place.price_per_night,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'number_rooms': place.number_rooms,
            'number_bathrooms': place.number_bathrooms,
            'max_guest': place.max_guest,
            'owner_id': place.user.id if hasattr(place.user, 'id') else place.user
        }, 200

