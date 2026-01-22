from flask_restx import Namespace, Resource, fields
import app.services.facade as facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'place_id': fields.String(required=True),
    'user_id': fields.String(required=True),
    'rating': fields.Integer(required=True),
    'comment': fields.String(required=True),
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(required=False),
    'comment': fields.String(required=False),
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String,
    'place_id': fields.String,
    'user_id': fields.String,
    'rating': fields.Integer,
    'comment': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
})


@api.route('/')
class ReviewList(Resource):

    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    @api.response(400, 'Validation error')
    def post(self):
        """Create new review"""
        data = api.payload
        try:
            review = facade.create_review(data)
        except ValueError as e:
            api.abort(400, str(e))

        return review, 201


    @api.marshal_list_with(review_response_model, code=200)
    def get(self):
        """Get all reviews"""
        try:
            reviews = facade.get_all_reviews()
        except ValueError as e:
            api.abort(400, str(e))

        return reviews, 200


@api.route('/<string:review_id>')
@api.response(404, 'Review not found')
class ReviewDetail(Resource):

    @api.marshal_with(review_response_model, code=200)
    def get(self, review_id):
        """Get review by ID"""
        try:
            review = facade.get_review_info(review_id)
        except ValueError as e:
            api.abort(404, str(e))

        return review, 200


    @api.expect(review_update_model, validate=False)
    @api.marshal_with(review_response_model, code=200)
    @api.response(400, 'Validation error')
    def put(self, review_id):
        """Update review by ID"""
        data = api.payload or {}

        try:
            updated = facade.update_review(review_id, data)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not updated:
            api.abort(404, "Review not found")

        return updated, 200


    @api.response(204, 'Review deleted')
    @api.response(400, 'Delete error')
    def delete(self, review_id):
        """Delete review by ID"""
        try:
            deleted = facade.delete_review(review_id)
        except ValueError as e:
            msg = str(e)
            if "not found" in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

        if not deleted:
            api.abort(404, "Review not found")

        return '', 204
