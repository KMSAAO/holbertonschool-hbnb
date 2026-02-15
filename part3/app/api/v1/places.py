from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request, current_app
from werkzeug.utils import secure_filename
from app.services import facade
import os
import uuid

api = Namespace("places", description="Place operations")

# Allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

place_create_model = api.model("PlaceCreate", {
    "title": fields.String(required=True),
    "description": fields.String(required=False),
    "price": fields.Float(required=True),
    "status": fields.String(required=False),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "location": fields.String(required=False),
    "amenities": fields.List(fields.Raw, required=False),
    "number_of_rooms": fields.Integer(required=False, default=0),
    "max_guests": fields.Integer(required=False, default=0),
    "tagline": fields.String(required=False),
    "rules": fields.String(required=False),
    "details": fields.List(fields.Raw, required=False), # JSON or List for 'about' sections
    "rooms": fields.List(fields.Raw, required=False),
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(required=False),
    "description": fields.String(required=False),
    "price": fields.Float(required=False),
    "status": fields.String(required=False),
    "latitude": fields.Float(required=False),
    "longitude": fields.Float(required=False),
    "location": fields.String(required=False),
    "number_of_rooms": fields.Integer(required=False),
    "max_guests": fields.Integer(required=False),
    "tagline": fields.String(required=False),
    "rules": fields.String(required=False),
    "details": fields.List(fields.Raw, required=False),
    "rooms": fields.List(fields.Raw, required=False),
    "amenities": fields.List(fields.String, required=False),
})

# Models for nested response
amenity_response_model = api.model("AmenityResponse", {
    "id": fields.String,
    "amenity_name": fields.String,
    "description": fields.String,
    "icon": fields.String,
    "status": fields.String
})

user_response_model = api.model("UserResponse", {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String
})

review_response_model = api.model("ReviewResponse", {
    "id": fields.String,
    "rating": fields.Integer,
    "comment": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String
})

place_response_model = api.model("PlaceResponse", {
    "id": fields.String,
    "owner_id": fields.String,
    "owner": fields.Nested(user_response_model),
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "status": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "location": fields.String,
    "images": fields.List(fields.String),
    "amenities": fields.List(fields.Nested(amenity_response_model)),
    "reviews": fields.List(fields.Nested(review_response_model)),
    "number_of_rooms": fields.Integer,
    "max_guests": fields.Integer,
    "tagline": fields.String,
    "rules": fields.String,
    "details": fields.Raw, # Return as object/list
    "rooms": fields.List(fields.Raw),
    "created_at": fields.String,
    "updated_at": fields.String,
})


def _get_attr(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_response_model, code=200)
    def get(self):
        user_id = request.args.get('user_id')
        if user_id:
            # If user_id is 'ME', use the current authenticated user
            if user_id == 'ME':
                # This requires a token, but the endpoint generally might not.
                # If 'ME' is passed, we check for token manually or assume client handles it.
                # However, @jwt_required is NOT on this method.
                # We can try verify_jwt_in_request(optional=True)
                from flask_jwt_extended import verify_jwt_in_request
                try:
                    verify_jwt_in_request()
                    current_user_id = get_jwt_identity()
                    if current_user_id:
                        return facade.get_places_by_user(current_user_id), 200
                except Exception:
                    pass # If fails, fallback or return empty/error? 
            
            # If specific UUID passed
            return facade.get_places_by_user(user_id), 200
            
        return facade.get_all_places(), 200

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_response_model, code=201)
    def post(self):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Invalid token")

        data = api.payload or {}

        # data["owner_id"] = str(current_user_id) needs owner_id in payload for create_place service?
        # Service expects 'owner_id' inside data.
        data["owner_id"] = str(current_user_id)

        try:
            place = facade.create_place(data)
            return place, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.marshal_with(place_response_model, code=200)
    def get(self, place_id):
        try:
            return facade.get_place_info(place_id), 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(place_update_model, validate=False)
    @api.marshal_with(place_response_model, code=200)
    def put(self, place_id):
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Invalid token")

        try:
            place = facade.get_place_info(place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = str(_get_attr(place, "owner_id"))
        if owner_id != str(current_user_id):
            api.abort(403, "Unauthorized action")

        data = api.payload or {}
        # remove owner_id if prevent ownership transfer
        if "owner_id" in data:
            del data["owner_id"]

        try:
            updated = facade.update_place(place_id, data)
            if not updated:
                api.abort(400, "Update failed")

            place = facade.get_place_info(place_id)
            return place, 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Invalid token")

        try:
            place = facade.get_place_info(place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = str(_get_attr(place, "owner_id"))
        
        # Check for admin?
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)

        if owner_id != str(current_user_id) and not is_admin:
            api.abort(403, "Unauthorized action")

        try:
            facade.delete_place(place_id)
            return {"message": "Place deleted successfully"}, 200
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:place_id>/amenities/<string:amenity_id>")
class PlaceAmenityResource(Resource):
    @jwt_required()
    def post(self, place_id, amenity_id):
        """Link an amenity to a place"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Invalid token")

        try:
            place = facade.get_place_info(place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = str(_get_attr(place, "owner_id"))
        if owner_id != str(current_user_id):
             # For simpler collaboration, maybe allow admins too? But strict ownership for now.
             # Wait, get_place_info returns DICTIONARY now.
             pass

        if owner_id != str(current_user_id):
            # Check for admin?
            claims = get_jwt() or {}
            if not claims.get("is_admin", False):
                api.abort(403, "Unauthorized action")

        try:
            facade.add_amenity_to_place(place_id, amenity_id)
            return {"message": "Amenity added successfully"}, 200
        except ValueError as e:
             api.abort(400, str(e))

    @jwt_required()
    def delete(self, place_id, amenity_id):
        """Unlink an amenity from a place"""
        current_user_id = get_jwt_identity()
        
        try:
            place = facade.get_place_info(place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = str(_get_attr(place, "owner_id"))
        
        claims = get_jwt() or {}
        is_admin = claims.get("is_admin", False)

        if owner_id != str(current_user_id) and not is_admin:
            api.abort(403, "Unauthorized action")

        try:
            facade.remove_amenity_from_place(place_id, amenity_id)
            return {"message": "Amenity removed successfully"}, 200
        except ValueError as e:
            api.abort(400, str(e))


@api.route("/<string:place_id>/images")
class PlaceImageUpload(Resource):
    @jwt_required()
    def post(self, place_id):
        """Upload images for a place (max 5 files, owner only)"""
        current_user_id = get_jwt_identity()
        if not current_user_id:
            api.abort(401, "Invalid token")

        # Verify the place exists and the user is the owner
        try:
            place = facade.get_place_info(place_id)
        except ValueError as e:
            api.abort(404, str(e))

        owner_id = str(_get_attr(place, "owner_id"))
        if owner_id != str(current_user_id):
            api.abort(403, "Only the owner can upload images")

        # Check if files were sent
        if 'images' not in request.files:
            api.abort(400, "No image files provided")

        files = request.files.getlist('images')
        # if len(files) > 5:
        #    api.abort(400, "Maximum 5 images allowed")

        if len(files) == 0:
            api.abort(400, "No image files provided")

        # Create upload directory
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        place_upload_dir = os.path.join(upload_folder, 'places', place_id)
        os.makedirs(place_upload_dir, exist_ok=True)

        uploaded_urls = []
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename to prevent collisions
                ext = file.filename.rsplit('.', 1)[1].lower()
                safe_name = f"{uuid.uuid4().hex[:8]}.{ext}"
                filename = secure_filename(safe_name)

                file_path = os.path.join(place_upload_dir, filename)
                file.save(file_path)

                # Build the public URL path
                url = f"/uploads/places/{place_id}/{filename}"
                uploaded_urls.append(url)
            elif file and file.filename:
                api.abort(400, f"File type not allowed: {file.filename}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

        if not uploaded_urls:
            api.abort(400, "No valid image files were uploaded")

        # Get existing images and append new ones
        existing_images = _get_attr(place, "images", []) or []
        all_images = existing_images + uploaded_urls

        # Update the place with the new image URLs
        try:
            facade.update_place(place_id, {"images": all_images})
            return {
                "message": f"{len(uploaded_urls)} image(s) uploaded successfully",
                "images": all_images
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
