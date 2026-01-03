import uuid

class User:
    def __init__(self, first_name, last_name, email):
        self.id = str(uuid.uuid4())  # إنشاء ID فريد تلقائياً
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
