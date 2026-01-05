from models.base_model import BaseModel


class Place(BaseModel):

    def __init__(self, title, description, price, status, latitude, longitude):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.status = status
        self.latitude = latitude
        self.longitude = longitude

        #implement these methods later
        def create_place(self):
            pass
        def get_place_info(self): 
            pass
        def update_place(self):
            pass
        def delete_place(self):
            pass