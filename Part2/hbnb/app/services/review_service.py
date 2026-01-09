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
            return None
        
        return review.id

    def update_Review(self, review_id, updated_data, repo):
        review = repo.get(review_id)
        if not review:
            return None
        
        forbidden_keys = ['id', 'created_at', 'updated_at']

        for key, value in updated_data.items():
            if key in forbidden_keys:
                return None
            
            if hasattr(review, key):
                setattr(review, key, value)

        review.last_updated()

        return review
    def delete_Review(self, review_id, repo):
        success = repo.delete(review_id)

        return success
    def get_all_reviews(self, repo):
        all_reviews = repo.get_all()
        if not all_reviews:
            return None

        return all_reviews
        