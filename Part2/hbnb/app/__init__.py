from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, title = "Hbnb API", description = "Hbnb Project API", version="1.0")

    return app
