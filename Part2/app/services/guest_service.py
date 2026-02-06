from app.models.guest import Guest


class GuestService():

    def register_as_guest(self, user, repo, bio=""):
        if not user or not hasattr(user, "id"):
            raise ValueError("Valid user object is required")

        new_guest = Guest(user=user, user_id=user.id, bio=bio)
        repo.add(new_guest)
        return new_guest

    def get_guest_info(self, guest_id, repo):
        if not isinstance(guest_id, str):
            raise ValueError("guest_id must be a string")

        guest = repo.get(guest_id)
        if not guest:
            raise ValueError("guest not found")

        return {
            "id": guest.id,
            "bio": guest.bio,
            "created_at": guest.created_at.isoformat(),
            "updated_at": guest.updated_at.isoformat()
        }

    def get_all_guests(self, repo):
        all_guests = repo.get_all()
        if not all_guests:
            return None
        return all_guests
        