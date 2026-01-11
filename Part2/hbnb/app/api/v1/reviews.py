from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user'), # ضروري جداً
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'text': fields.String(required=True, description='Review content') # text وليس comment
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(description='Updated rating'),
    'text': fields.String(description='Updated content')
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(readonly=True),
    'place_id': fields.String(),
    'user_id': fields.String(),
    'rating': fields.Integer(),
    'text': fields.String(),
    'created_at': fields.DateTime(),
    'updated_at': fields.DateTime()
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        """Create a new review"""
        try:
            return facade.create_review(api.payload), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(review_response_model, code=200)
    def get(self):
        """Get all reviews"""
        return facade.get_all_reviews(), 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_response_model)
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review, 200

    @api.expect(review_update_model)
    @api.marshal_with(review_response_model)
    def put(self, review_id):
        """Update a review"""
        try:
            return facade.update_review(review_id, api.payload), 200
        except ValueError as e:
            api.abort(404, str(e))

    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return '', 204
        except ValueError as e:
            api.abort(404, str(e))