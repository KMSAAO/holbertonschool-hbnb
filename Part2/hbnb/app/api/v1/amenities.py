# app/api/v1/amenities.py
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_create_model = api.model('AmenityCreate', {
    'amenity_name': fields.String(required=True, description='Amenity name'),
    'description':  fields.String(required=False, description='Description'),
    'status':       fields.String(required=False, description='Status (ACTIVE / INACTIVE)'),
})

amenity_update_model = api.model('AmenityUpdate', {
    'amenity_name': fields.String(required=False, description='Amenity name'),
    'description':  fields.String(required=False, description='Description'),
    'status':       fields.String(required=False, description='Status (ACTIVE / INACTIVE)'),
})

amenity_response_model = api.model('AmenityResponse', {
    'id':           fields.String(required=True, description='Amenity ID'),
    'amenity_name': fields.String(required=True, description='Amenity name'),
    'description':  fields.String(required=False, description='Description'),
    'status':       fields.String(required=True, description='Status'),
})


# ====== /api/v1/amenities ======

@api.route('/')
class AmenityList(Resource):

    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_response_model, code=201)
    @api.response(400, 'Validation / business error')
    def post(self):
        """
        Create new amenity
        """
        amenity_data = api.payload

        try:
            amenity = facade.create_amenity(amenity_data)

            if hasattr(amenity, "to_dict"):
                return amenity.to_dict(), 201

            return {
                "id": amenity.id,
                "amenity_name": amenity.amenity_name,
                "description": amenity.description,
                "status": amenity.status.value if hasattr(amenity.status, "value") else amenity.status,
            }, 201

        except ValueError as ex:
            api.abort(400, str(ex))


# ====== /api/v1/amenities/<amenity_id> ======

@api.route('/<string:amenity_id>')
class AmenityDetail(Resource):

    @api.marshal_with(amenity_response_model, code=200)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity by ID
        """
        try:
            amenity_dict = facade.get_amenity_info(amenity_id)
            return amenity_dict, 200
        except ValueError as ex:
            api.abort(404, str(ex))

    @api.expect(amenity_update_model, validate=False)
    @api.marshal_with(amenity_response_model, code=200)
    @api.response(400, 'Validation / business error')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """
        Update amenity
        """
        data = api.payload or {}

        try:
            facade.update_amenity(amenity_id, data)
            updated = facade.get_amenity_info(amenity_id)
            return updated, 200

        except ValueError as ex:
            msg = str(ex)
            if "not found" in msg:
                api.abort(404, msg)
            api.abort(400, msg)

    @api.response(204, 'Amenity deleted')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """
        Delete amenity
        """
        try:
            deleted = facade.delete_amenity(amenity_id)
            if not deleted:
                api.abort(404, "Amenity not found")
            return '', 204
        except ValueError as ex:
            msg = str(ex)
            if "not found" in msg:
                api.abort(404, msg)
            api.abort(400, msg)
