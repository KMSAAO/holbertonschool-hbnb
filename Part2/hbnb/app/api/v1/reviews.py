from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'comment': fields.String(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    def post(self):
        try:
            review = facade.create_review(api.payload)
            return {'id': review.id, 'status': 'Review created'}, 201
        except ValueError as e:
            return {'error': str(e)}, 400
