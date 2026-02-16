from app.models.guest import Guest


class GuestService():

    def register_as_guest(self, user: dict, guest_db, bio=""):

        print("DEBUG bio value:", bio)
        print("DEBUG bio type:", type(bio))
        user_id = user.get("user_id")
        if not user_id:
            raise ValueError("Valid user_id is required")

        new_guest = Guest(user_id=user_id, bio=bio)
        guest_db.add(new_guest)
        return new_guest

    def get_all_guests(self, repo):
        all_guests = repo.get_all()
        if not all_guests:
            return None
        return all_guests
        

    def get_all_guests(self, repo):
        all_guests = repo.get_all()
        if not all_guests:
            return None
        return all_guests
        