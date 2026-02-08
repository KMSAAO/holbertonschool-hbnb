from flask import Flask, app, jsonify
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
from app.models.user import User

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

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

    @app.route("/")
    def index():
        return jsonify({"message": "HBnB API is running"})

    return app


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    user_id = jwt_data.get("sub")
    if not user_id:
        return None

    return User.query.get(user_id)
