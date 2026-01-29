from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'rating': fields.Integer(required=True, description='Rating value'),
    'comment': fields.String(required=True, description='Review comment'),
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(required=False, description='Updated rating value'),
    'comment': fields.String(required=False, description='Updated review comment'),
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String,
    'place_id': fields.String,
    'user_id': fields.String,
    'rating': fields.Integer,
    'comment': fields.String
})


def _get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@api.route('/')
class ReviewList(Resource):

    @api.marshal_list_with(review_response_model, code=200)
    def get(self):
        """Get all reviews (public)"""
        try:
            return facade.get_all_reviews(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    @api.response(400, 'Validation / business error')
    def post(self):
        """Create a new review (authenticated)
        - user cannot review own place
        - user can only create one review per place
        """
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Missing/invalid token")

        data = api.payload or {}
        place_id = data.get("place_id")
        if not place_id:
            api.abort(400, "place_id is required")

        try:
            place = facade.get_place_info(place_id=place_id)
        except ValueError:
            api.abort(400, "Place not found")

        place_owner_id = _get_attr(place, "owner_id")
        if str(place_owner_id) == str(current_user_id):
            api.abort(400, "You cannot review your own place.")

        try:
            all_reviews = facade.get_all_reviews() or []
        except ValueError:
            all_reviews = []

        for r in all_reviews:
            r_place_id = _get_attr(r, "place_id")
            r_user_id = _get_attr(r, "user_id")
            if str(r_place_id) == str(place_id) and str(r_user_id) == str(current_user_id):
                api.abort(400, "You have already reviewed this place.")

        payload = {
            "place_id": str(place_id),
            "user_id": str(current_user_id),
            "rating": data.get("rating"),
            "comment": data.get("comment"),
        }

        try:
            review = facade.create_review(payload)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    @api.marshal_with(review_response_model, code=200)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID (public)"""
        try:
            review = facade.get_review_info(review_id)
            return review, 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(review_update_model, validate=False)
    @api.marshal_with(review_response_model, code=200)
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update review (only author)"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Missing/invalid token")

        try:
            review = facade.get_review_info(review_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = _get_attr(review, "user_id")
        if str(owner_id) != str(current_user_id):
            api.abort(403, "Unauthorized action.")

        data = api.payload or {}
        try:
            updated = facade.update_review(review_id, data)
            return updated, 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(204, 'Review deleted')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete review (only author)"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Missing/invalid token")

        try:
            review = facade.get_review_info(review_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = _get_attr(review, "user_id")
        if str(owner_id) != str(current_user_id):
            api.abort(403, "Unauthorized action.")

        try:
            facade.delete_review(review_id)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))
