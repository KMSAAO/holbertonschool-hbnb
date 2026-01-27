from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'user_id': fields.String(required=True, description='ID of the review author'),
    'rating': fields.Integer(required=True, description='Rating value'),
    'comment': fields.String(required=True, description='Review comment'),
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(required=False, description='Updated rating value'),
    'comment': fields.String(required=False, description='Updated review comment'),
})

review_response_model = api.model('ReviewResponse', {
   'id': fields.String,
   'place_id' : fields.String,
   'user_id'  : fields.String,
   'rating'   : fields.Integer,
   'comment'  : fields.String
})


@api.route('/')
class ReviewList(Resource):

    @api.marshal_list_with(review_response_model, code=200)
    def get(self):
        """Get all reviews"""
        try:
            return facade.get_all_reviews(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Validation / business error')
    def post(self):
        """Create a new review (authenticated user)"""
        claims = get_jwt() or {}
        user_id = claims.get("id")
        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        review_data = api.payload or {}
        review_data["user_id"] = str(user_id)  # enforce from token

        try:
            review = facade.create_review(review_data)
            return review, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    @api.marshal_with(review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
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
        """Update review (owner only, admin bypass)"""
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)
        user_id = claims.get("id")

        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        try:
            review = facade.get_review_info(review_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = review.get("user_id") if isinstance(review, dict) else getattr(review, "user_id", None)

        if not is_admin and str(owner_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        try:
            review_data = api.payload or {}
            updated = facade.update_review(review_id, review_data)
            return updated, 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(204, 'Review deleted')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Delete error')
    def delete(self, review_id):
        """Delete a review (owner only, admin bypass)"""
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)
        user_id = claims.get("id")

        if not user_id:
            api.abort(401, "Invalid token: missing user id")

        try:
            review = facade.get_review_info(review_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = review.get("user_id") if isinstance(review, dict) else getattr(review, "user_id", None)

        if not is_admin and str(owner_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        try:
            facade.delete_review(review_id)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))
