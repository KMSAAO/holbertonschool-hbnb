from app.models.review import Review

class ReviewService:
    def create_review(self, review_data, place_repo, review_repo, user_repo):
        place_id = review_data.get("place_id")
        user_id  = review_data.get("user_id")
        rating   = review_data.get("rating")
        text     = review_data.get("text")

        place = place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        user = user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        review = Review(text=text, rating=rating, place=place, user=user)
        
        review_repo.add(review)
        return review

    def get_review_info(self, review_id, review_repo):
        review = review_repo.get(review_id)
        if not review:
             raise ValueError("Review not found")
        return review

    def get_all_reviews(self, review_repo):
        return review_repo.get_all()

    def update_review(self, review_id, review_data, review_repo):
        review = review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        review_repo.update(review_id, review.to_dict())
        return review

    def delete_review(self, review_id, review_repo):
        review = review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        review_repo.delete(review_id)