from app.models.guest import Guest


class GuestService():

    def register_as_guest(self,user_data: dict, repo, bio):

        user_id = user_data.get('user_id')
        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id is required and must be a string")
        
        bio = user_data.get('bio')
        if not bio or not isinstance(bio, str) or len(bio) > 100:
            raise ValueError("bio is required and must be a string with max 100 characters")
        
        new_guest = Guest(bio = bio)
        repo.add(new_guest)
        return new_guest

    def get_guest_info(self, guest_id, repo):
            
        if not isinstance(guest_id, str):
            raise ValueError("guest_id ID must be a string")

        guest = repo.get(guest_id)
        if not guest:
            raise ValueError("guest not found")


        return {
            "id": guest.id,
            "bio": guest.bio,
            "created_at": guest.created_at.isoformat(),
            "updated_at": guest.updated_at.isoformat()}