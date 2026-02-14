from flask import Flask, app, jsonify, render_template
from flask_restx import Api

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.guests import api as guests_ns
from app.api.v1.bookings import api as bookings_ns

from app.bcrypt import bcrypt
from app.JWTManger import jwt  
from app.db import db
import app.services.facade as facade
from flask_cors import CORS

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    @app.route("/", strict_slashes=False)
    def index():
        return render_template("index.html")

    @app.route("/places", strict_slashes=False)
    def places():
        return render_template("places.html")

    @app.route("/login", strict_slashes=False)
    def login():
        return render_template("login.html")

    @app.route("/admin", strict_slashes=False)
    def admin():
        return render_template("admin.html")
    @app.route("/bookings", strict_slashes=False)
    def bookings():
        return render_template("bookings.html")
    @app.route("/profile", strict_slashes=False)
    def profile():
        return render_template("profile.html")
    @app.route("/forgot_password", strict_slashes=False)
    def forgot_password():
        return render_template("forgot_password.html")
    @app.route("/hotel-details", strict_slashes=False)
    def hotel_details():
        return render_template("hotel-details.html")
    @app.route("/reservation", strict_slashes=False)
    def reservation():
        return render_template("reservation.html")

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)


    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/docs',
        authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': "Bearer <JWT>"
            }
        },
        security='Bearer Auth'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(guests_ns,path= '/api/v1/guests')
    api.add_namespace(bookings_ns,path='/api/v1/bookings')


    return app

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Optional: used by flask-jwt-extended if you want current_user auto loading.
    We keep it safe: return None if user not found.
    """
    identity = jwt_data.get("sub")
    if not identity:
        return None

    try:
        user = facade.get_user(identity)
        return user  
    except Exception:
        return None
