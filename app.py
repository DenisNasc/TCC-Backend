import os

from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import JWT


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'sqlite:///{os.path.join(basedir, "data.sqlite")}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_AUTH_USERNAME_KEY"] = "email"
app.config["JWT_AUTH_URL_RULE"] = "/v1/auth"
app.config["SECRET_KEY"] = "SUPER-SECRETO"

app_context = app.app_context()
app_context.push()

# BANCO DE DADOS
db = SQLAlchemy(app)
api = Api(app)

g.db = db
g.api = api
migrate = Migrate(app, db)

# ROTAS
from routes.users import Users
from routes.projects import Projects
from routes.stations import Stations
from routes.coordinates import Coordinates


from security import authenticate, identity

jwt = JWT(app, authenticate, identity)


api.add_resource(
    Users,
    "/v1/users",
    "/v1/users/<id>",
)
api.add_resource(
    Projects,
    "/v1/users/<user_id>/projects",
    "/v1/users/<user_id>/projects/<id>",
)

api.add_resource(
    Stations,
    "/v1/users/<user_id>/projects/<project_id>/stations",
    "/v1/users/<user_id>/projects/<project_id>/stations/<station_id>",
)

api.add_resource(
    Coordinates,
    "/v1/users/<user_id>/projects/<project_id>/stations/<station_id>/coordinates",
    "/v1/users/<user_id>/projects/<project_id>/stations/<station_id>/coordinates/<coordinate_id>",
)


if __name__ == "__main__":
    app.run(debug=True)
