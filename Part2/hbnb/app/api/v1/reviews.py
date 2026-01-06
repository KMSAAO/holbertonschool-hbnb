from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review content'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5'),
    'user_id': fields.String(required=True, description='ID of the reviewer'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    def post(self):
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return {'id': new_review.id, 'text': new_review.text}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        reviews = facade.get_all_reviews()
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200
