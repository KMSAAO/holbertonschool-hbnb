from flask_jwt_extended import current_user
from app.models.guest import Guest


class GuestService():

    def register_as_guest(self, user: dict, guest_db, bio=""):

        user_id = user.get("user_id")
        if not user_id:
            raise ValueError("Valid user_id is required")

        new_guest = Guest(user_id=user_id, bio=bio)
        guest_db.add(new_guest)
        return new_guest
    
    def get_guest_by_user_id(self, user_id, current_user, guest_repo, user_repo):

        user = user_repo.get(current_user)
        if not user:
            raise PermissionError("Forbidden")

        if user.is_admin:
            guest = guest_repo.get_by_user_id(user_id)
            if not guest:
                raise ValueError("Guest not found")
            return guest

        if current_user != user_id:
            raise PermissionError("Forbidden")

        guest = guest_repo.get_by_user_id(user_id)
        if not guest:
            raise ValueError("Guest not found")

        return guest

    def get_all_guests(self, current_user, guest_repo, user_repo):

        user = user_repo.get(current_user)
        if not user or not user.is_admin:
            raise PermissionError("Forbidden")

        return guest_repo.get_all()
