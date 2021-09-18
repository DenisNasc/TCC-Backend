from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from models import db

from config import config

from routes.errors import errors

cors = CORS()
jwt = JWTManager()
migrate = Migrate()
bcrypt = Bcrypt()
api = Api(errors=errors)


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bcrypt.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    from routes import initialize_routes
    from resources.auth import initialize_auth_routes

    initialize_routes(api)
    initialize_auth_routes(app)

    api.init_app(app)

    return app
