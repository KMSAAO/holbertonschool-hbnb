from app.models.guest import Guest


class GuestService():

    def register_as_guest(self, user, repo, bio=""):

        if not user or not hasattr(user, "id"):
            raise ValueError("Valid user object is required")

        if not isinstance(bio, str) or len(bio) > 100:
            raise ValueError("bio must be a string with max 100 characters")

        new_guest = Guest(user=user, user_id=user.id, bio=bio)

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