from app.models.review import Review

class Review_Service:
    def create_review(self, review_data, review_repo, user_repo, place_repo):
        user = user_repo.get(review_data.get('user_id'))
        place = place_repo.get(review_data.get('place_id'))
        
        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")
        
        rating = review_data.get('rating')
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
            
        new_review = Review(**review_data)
        review_repo.add(new_review)
        return new_review

    def get_review_info(self, review_id, repo):
        return repo.get(review_id)

    def get_all_reviews(self, repo):
        return repo.get_all()
