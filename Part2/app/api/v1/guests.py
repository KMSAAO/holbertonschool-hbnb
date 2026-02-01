from flask_restx import Namespace, Resource, fields
import app.services.facade as facade

api = Namespace('guest', description='guest operations')

user_register_model = api.model('register_as_guest',
    {

    })