from app.models.guest import Guest


class GuestService():

    def register_as_guest(self, user: dict, bio=""):
        user_id = user.get("user_id")

        if not user_id:
            raise ValueError("Valid user_id is required")

        new_guest = Guest(user_id=user_id, bio=bio)
        return self.guest_repo.add(new_guest)

    def get_all_guests(self, repo):
        all_guests = repo.get_all()
        if not all_guests:
            return None
        return all_guests
        