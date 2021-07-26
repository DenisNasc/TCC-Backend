from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt import jwt_required

from models.users import User
from models.projects import Project
from models.stations import Station

from uuid import uuid4

db = g.db

stations_fields = {
    "id": fields.String,
    "name": fields.String,
    "longitudinal": fields.Float,
    "createdAt": fields.DateTime,
    "updateddAt": fields.DateTime,
}

response_fields = {
    "stations": fields.List(fields.Nested(stations_fields)),
    "projectID": fields.String,
    "userID": fields.String,
    "message": fields.String,
}


def init_args(fields):
    parser = reqparse.RequestParser()

    for field in fields:
        parser.add_argument(field)

    args = parser.parse_args()
    return args


class Stations(Resource):
    @marshal_with(response_fields)
    def get(self, user_id, project_id, station_id=None):
        try:
            if not User.query.filter_by(id=user_id).first():
                return {"message": "Usuário não cadastrado"}, 404, {}

            if not Project.query.filter_by(id=project_id).first():
                return {"message": "Projeto inexistente"}, 404, {}

            if not station_id:
                stations = Station.query.filter_by(
                    projectID=project_id, userID=user_id
                ).all()

                response = {
                    "stations": stations,
                    "userID": user_id,
                    "projectID": project_id,
                    "message": "Não há balizas para esse projeto",
                }
                return response, 200, {}

            station = Station.query.filter_by(
                projectID=project_id, userID=user_id, id=station_id
            ).all()

            response = {
                "stations": station,
                "userID": user_id,
                "projectID": project_id,
            }

            return response, 200, {}

        except:
            return {"message": "Error inesperado no servidor"}, 500, {}

    @marshal_with(response_fields)
    def post(self, user_id, project_id):
        try:
            fields = ("name", "longitudinal")

            args = init_args(fields)

            if not User.query.filter_by(id=user_id).first():
                return {"message": "Usuário não cadastrado"}, 404, {}

            if not Project.query.filter_by(id=project_id).first():
                return {"message": "Projeto inexistente"}, 404, {}

            args["id"] = str(uuid4())
            args["userID"] = user_id
            args["projectID"] = project_id

            new_station = Station(**args)

            db.session.add(new_station)
            db.session.commit()

            stations = Station.query.filter_by(
                userID=user_id, projectID=project_id
            ).all()

            response = {
                "stations": stations,
                "userID": user_id,
                "projectID": project_id,
            }

            return response, 201, {}

        except:
            return {"message": "Error inesperado no servidor"}, 500, {}
