from app.models.user import User

class User_Service():
    def register_users(self, user_data, repo):
        existing_user = repo.get_by_attribute('email', user_data.get('email'))
        if existing_user:
            raise ValueError("Email already registered")
        
        user = User(**user_data)
        repo.add(user)
        return user

    def get_user_info(self, user_id, repo):
        user = repo.get(user_id)
        if not user:
            return None
        return user

    def update_users(self, user_id, update_data, repo):
        user = repo.get(user_id)
        if not user:
            return None
        
        forbidden_keys = ['id', 'created_at', 'updated_at', 'email']
        for key, value in update_data.items():
            if key not in forbidden_keys and hasattr(user, key):
                setattr(user, key, value)
        
        user.last_updated()
        return user

    def get_all_users(self, repo):
        return repo.get_all()
