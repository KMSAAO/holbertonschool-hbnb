from app.models.review import Review

class Review_Service():
    def create_Review(self, review_data, repo):
        rating = review_data.get('rating')
        comment = review_data.get('comment')
        if type(rating) != int and rating <= 5:
            raise ValueError("Rating value is not correct")
        
        if len(comment) > 250:
            raise ValueError("Comment is too long")
        
        review = Review(**review_data)
        repo.add(review)

        return review

    def get_Review_info(self, review_id, repo): 
        review = repo.get(review_id)

        if not review:
            return None
        
        return review

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
        