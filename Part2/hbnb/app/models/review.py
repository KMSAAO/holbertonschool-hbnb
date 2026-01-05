from models.base_model import BaseModel

class Review(BaseModel):

    def __init__(self, rating, comment):
        super().__init__()
        self.rating = rating
        self.comment = comment

    
     #implement these methods later
        def create_Review(self):
            pass
        def get_Review_info(self): 
            pass
        def update_Review(self):
            pass
        def delete_Review(self):
            pass
        def get_all_reviews(self):
            pass