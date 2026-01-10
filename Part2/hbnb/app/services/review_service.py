from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class ReviewService():

    def create_Review(self, review_data: dict, repo):

        rating = review_data.get('rating')

        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        comment = review_data.get("comment")

        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment is required and must be a non-empty string")

        if len(comment) > 250:
            raise ValueError("Comment must not exceed 250 characters")

        palce = review_data.get('place') 

        review = Review(place = palce, rating = rating, comment = comment)

        repo.add(review)

        return review

    def get_Review_info(self, review_id, repo):
        review = repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return {
        "id": review.id,
        "place_id": review.place_id,
        "user_id": review.place.user_id,
        "Onwer review": review.place.user.first_name,
        "rating": review.rating,
        "comment": review.comment,
        "created at": review.created_at,
        "updated at": review.updated_at
    }


    def update_review(self, review_id, updated_data, repo):
        review = repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        if 'rating' in updated_data:
            rating = updated_data['rating']
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        review["rating"] = rating

        if 'comment' in updated_data:
            comment = updated_data['comment']
        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment must be a non-empty string")
        if len(comment) > 250:
            raise ValueError("Comment must not exceed 250 characters")
        review["comment"] = comment

        if 'place_id' in updated_data:
            place_id = updated_data['place_id']
        if not isinstance(place_id, str):
            raise ValueError("place_id must be a string")
        review["place_id"] = place_id

        if 'user_id' in updated_data:
            user_id = updated_data['user_id']
        if not isinstance(user_id, str):
            raise ValueError("user_id must be a string")
        review["user_id"] = user_id

        return review

    def delete_Review(self, review_id, repo):
        Deleted = repo.delete(review_id)
        return Deleted

    def get_all_reviews(self, repo):
        all_reviews = repo.get_all()
        if not all_reviews:
            return None

        return all_reviews
        