from flask import Blueprint
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, title='HBnB API', version='1.0', description='HBnB Application API endpoints')

api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
