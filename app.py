from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


from resources.errors import errors
from database.db import initialize_db

from config import DevConfig

bcrypt = Bcrypt()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app_context = app.app_context()
    app_context.push()

    bcrypt.init_app(app)

    CORS(app)
    JWTManager(app)

    db = initialize_db(app)
    g.db = db

    api = Api(app, errors=errors)

    from resources.routes import initialize_routes
    from resources.auth import initialize_auth_routes

    initialize_routes(api)
    initialize_auth_routes(app)

    return app


if __name__ == "__main__":
    app = create_app(DevConfig)
    app.run()
