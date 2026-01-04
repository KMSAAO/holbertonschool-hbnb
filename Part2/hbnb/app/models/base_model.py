import uuid, datetime

class BaseModel:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def last_updated(self):
        self.updated_at = datetime.now()