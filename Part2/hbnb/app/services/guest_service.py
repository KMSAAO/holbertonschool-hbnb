from app.models.guest import guest


class GuestService():

    def register_as_guest(self,user_id,user_data: dict, repo, bio):

        user_id = user_data.get('user_id')
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id is required and must be a string")
        
        bio = user_data.get('bio')
        if not bio or not isinstance(bio, str) or len(bio) > 100:
            raise ValueError("bio is required and must be a string with max 100 characters")
        
        Guest = guest(bio = bio)
        repo.add(guest)
        return guest
    