from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt import jwt_required

from models.users import User
from models.projects import Project
from models.stations import Station

from uuid import uuid4

db = g.db

coordinates_fields = {
    "id": fields.String,
    "type": fields.String,
    "vertical": fields.Float,
    "transversal": fields.Float,
    "createdAt": fields.DateTime,
    "updateddAt": fields.DateTime,
}

response_fields = {
    "coordinates": fields.List(fields.Nested(coordinates_fields)),
    "stationID": fields.String,
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


class Coordinates(Resource):
    @marshal_with(response_fields)
    def get(self, user_id, project_id, station_id, coordinate_id=None):
        try:
            if not User.query.filter_by(id=user_id).first():
                return {"message": "Usuário não cadastrado"}, 404, {}

            if not Project.query.filter_by(id=project_id).first():
                return {"message": "Projeto inexistente"}, 404, {}

            if not Station.query.filter_by(id=station_id).first():
                return {"message": "Baliza inexistente"}, 404, {}

            if not coordinate_id:
                coordinates = Coordinates.query.filter_by(
                    projectID=project_id, userID=user_id, stationID=station_id
                ).all()

                response = {
                    "coordinates": coordinates,
                    "stationID": station_id,
                    "projectID": project_id,
                    "userID": user_id,
                }

                return response, 200, {}

            coordinate = Coordinates.query.filter_by(
                projectID=project_id,
                userID=user_id,
                stationID=station_id,
                id=coordinate_id,
            ).all()

            response = {
                "coordinates": coordinate,
                "stationID": station_id,
                "projectID": project_id,
                "userID": user_id,
            }

            return response, 200, {}

        except:
            return {"message": "Erro inesperado no servidor"}, 500, {}
