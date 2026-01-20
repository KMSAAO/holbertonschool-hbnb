from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class ReviewService():

    def create_Review(self, review_data, place_repo, review_repo):
        place_id = review_data.get("place_id")
        rating   = review_data.get("rating")
        comment  = review_data.get("comment")

        place = place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found")

        user_id = place.user.id
        review = Review(place_id=place_id, user_id=user_id, rating=rating, comment=comment)
        review_repo.add(review)

        return review

    def get_review_info(self, review_id, review_repo):
        review = review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review.to_dict()

    def update_review(self, review_id: str, review_data: dict, review_repo):

        if not isinstance(review_id, str):
            raise ValueError("review_id must be a string")

        review = review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        if "rating" in review_data:
            review.rating = review_data["rating"]

        if "comment" in review_data:
            review.comment = review_data["comment"]

        review_repo.update(
            review_id,
            {
                "rating": review.rating,
                "comment": review.comment
            }
        )

        return review

    def delete_Review(self, review_id, review_repo):
        if not review_id or not isinstance(review_id, str):
            raise TypeError("review_id must be required")

        Deleted = review_repo.delete(review_id)
        return Deleted

    def get_all_reviews(self, repo):
        all_reviews = repo.get_all()
        if not all_reviews:
            return None

        return all_reviews 