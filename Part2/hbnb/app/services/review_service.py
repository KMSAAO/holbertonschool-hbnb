from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class ReviewService():

    def create_Review(self, review_data, place_repo, review_repo):
        place_id = review_data.get("place_id")
        rating   = review_data.get("rating")
        comment  = review_data.get("comment")

        if not isinstance(place_id, str):
            raise ValueError("Place ID must be a string")

        place = place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found")

        if not isinstance(rating, int):
            raise ValueError("rating must be a integer")
        
        if rating <= 0 or rating >= 6:
            raise ValueError("rating must be between 1 to 5")

        review = Review(place=place, rating=rating, comment=comment)
        review_repo.add(review)

        return review_data

    def get_review_info(self, review_id: str, review_repo):
        if not isinstance(review_id, str):
            raise ValueError("Review ID must be a string")

        review = review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        return {
            "id": review.id,
            "place_id": review.place_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
        }


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


    def delete_Review(self, review_id, repo):
        Deleted = repo.delete(review_id)
        return Deleted

    def get_all_reviews(self, repo):
        all_reviews = repo.get_all()
        if not all_reviews:
            return None

        return all_reviews 