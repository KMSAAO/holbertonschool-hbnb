# app/api/v1/reviews.py
from flask_restx import Namespace, Resource, fields

from app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'place_id': fields.String(
        required=True,
        description='ID of the place being reviewed'
    ),
    'rating': fields.Integer(
        required=True,
        description='Rating value'
    ),
    'comment': fields.String(
        required=True,
        description='Review comment'
    ),
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(
        required=False,
        description='Updated rating value'
    ),
    'comment': fields.String(
        required=False,
        description='Updated review comment'
    ),
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(
        readonly=True,
        description='Review ID'
    ),
    'place_id': fields.String(
        description='ID of the place being reviewed'
    ),
    'rating': fields.Integer(
        description='Rating value'
    ),
    'comment': fields.String(
        description='Review comment'
    ),
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Validation / business error')
    def post(self):
        """Create a new review"""
        review_data = api.payload

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
        """Get a single review by ID"""
        try:
            review = facade.get_review_info(review_id)
            return review, 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(review_update_model, validate=False)
    @api.marshal_with(review_response_model, code=200)
    def put(self, review_id):
        try:
            review_data = api.payload or {}
            review = facade.update_review(review_id, review_data)
            return review, 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.response(204, 'Review deleted')
    @api.response(400, 'Delete error')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))
