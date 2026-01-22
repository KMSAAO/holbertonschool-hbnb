import bcrypt
from flask import Flask, jsonify
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns
from app.bcrypt import bcrypt

def create_app(config_class="config.DevelopmentConfig"):
    
    app = Flask(__name__)

    app.config.from_object(config_class)

    bcrypt.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/docs'
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    @app.route("/")
    def index():
        return jsonify({"message": "HBnB API is running"})

    return app