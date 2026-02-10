from app.models.guest import Guest


class GuestService():

    def register_as_guest(self, user: dict, guest_db, bio=""):

        user_id = user.get("user_id")
        if not user_id:
            raise ValueError("Valid user_id is required")

        new_guest = Guest(user_id=user_id, bio=bio)
        guest_db.add(new_guest)
        return new_guest
    
    def get_guest_by_user_id(self, user_id, repo):
        guest = repo.get_by_user_id(user_id)
        if not guest:
            raise ValueError("Guest not found")
        return guest

    def get_all_guests(self, repo):
        all_guests = repo.get_all()
        if not all_guests:
            return None
        return all_guests