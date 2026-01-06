from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    def get(self):
        """List all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    def post(self):
        """Create a new amenity"""
        new_amenity = facade.create_amenity(api.payload)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201
