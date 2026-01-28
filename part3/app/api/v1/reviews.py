from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_create_model = api.model('ReviewCreate', {
    'place_id': fields.String(required=True),
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
   'comment': fields.String
})


@api.route('/')
class ReviewList(Resource):

    @api.marshal_list_with(review_response_model, code=200)
    def get(self):
        return facade.get_all_reviews(), 200

    @jwt_required()
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_response_model, code=201)
    def post(self):
        claims = get_jwt()
        user_id = claims.get("id")

        review_data = api.payload
        review_data["user_id"] = user_id

        place = facade.get_place_info(review_data["place_id"])
        if place["owner_id"] == user_id:
            api.abort(400, "Cannot review your own place")

        all_reviews = facade.get_all_reviews()
        for r in all_reviews:
            if r["place_id"] == review_data["place_id"] and r["user_id"] == user_id:
                api.abort(400, "Already reviewed this place")

        review = facade.create_review(review_data)
        return review, 201


@api.route('/<string:review_id>')
class ReviewResource(Resource):

    @api.marshal_with(review_response_model, code=200)
    def get(self, review_id):
        review = facade.get_review_info(review_id)
        return review, 200

    @jwt_required()
    @api.expect(review_update_model, validate=False)
    @api.marshal_with(review_response_model, code=200)
    def put(self, review_id):
        claims = get_jwt()
        user_id = claims.get("id")
        is_admin = claims.get("is_admin", False)

        review = facade.get_review_info(review_id)
        if not is_admin and review["user_id"] != user_id:
            api.abort(403, "Unauthorized action")

        facade.update_review(review_id, api.payload)
        updated = facade.get_review_info(review_id)
        return updated, 200

    @jwt_required()
    def delete(self, review_id):
        claims = get_jwt()
        user_id = claims.get("id")
        is_admin = claims.get("is_admin", False)

        review = facade.get_review_info(review_id)
        if not is_admin and review["user_id"] != user_id:
            api.abort(403, "Unauthorized action")

        facade.delete_review(review_id)
        return '', 204
