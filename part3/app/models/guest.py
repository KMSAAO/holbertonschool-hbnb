from app.db import db
from app.models.base_model import BaseModel
from app.models.user import User

class Guest(BaseModel):
    __tablename__ = "guests"

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    _bio = db.Column("bio", db.String(255), nullable=True)  # ← هذا التغيير المهم

    user = db.relationship("User", backref="guest", lazy=True)

    def __init__(self, user_id: str, bio: str = ""):
        super().__init__()
        self.user_id = user_id
        self.bio = bio

    @property
    def bio(self):
        return self._bio

    @bio.setter
    def bio(self, value):
        if not isinstance(value, str):
            raise ValueError("Bio must be a string.")
        self._bio = value
