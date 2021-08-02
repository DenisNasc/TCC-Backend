from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from uuid import uuid4

from services.init_args import init_args

from database.models.users import UserModel
from database.models.projects import ProjectModel
from database.models.stations import StationModel
from database.models.coordinates import CoordinateModel


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
    "userID": fields.String,
    "projectID": fields.String,
    "stationID": fields.String,
    "message": fields.String,
}


class CoordinatesApi(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id, station_id):
        try:
            coordinates = CoordinateModel.query.filter_by(
                userID=user_id, projectID=project_id, stationID=station_id
            ).all()

            response = {
                "coordinates": coordinates,
            }

            return response, 200, {}

        except:
            return {"message": "Erro inesperado no servidor"}, 500, {}

    @jwt_required()
    @marshal_with(response_fields)
    def post(self, user_id, project_id, station_id):
        try:
            fields = ("type", "vertical", "transversal")

            args = init_args(fields)

            if not UserModel.query.filter_by(id=user_id).first():
                return {"message": "Usuário não cadastrado"}, 404, {}

            if not ProjectModel.query.filter_by(id=project_id).first():
                return {"message": "Projeto inexistente"}, 404, {}

            if not StationModel.query.filter_by(id=station_id).first():
                return {"message": "Baliza inexistente"}, 404, {}

            args["id"] = str(uuid4())
            args["userID"] = user_id
            args["projectID"] = project_id
            args["stationID"] = station_id

            new_coordinate = CoordinateModel(**args)

            db.session.add(new_coordinate)
            db.session.commit()

            print("oi")
            coordinates = CoordinateModel.query.filter_by(
                userID=user_id, projectID=project_id, stationID=station_id
            ).all()

            response = {
                "coordinates": coordinates,
                "userID": user_id,
                "projectID": project_id,
                "stationID": station_id,
            }

            return response, 201, {}

        except:
            return {"message": "Erro inesperado no servidor"}, 500, {}


class CoordinateApi(Resource):
    def get(self, user_id, project_id, station_id, coordinate_id):
        try:
            if station_id and not UserModel.query.filter_by(id=user_id).first():
                return {"message": "Usuário não cadastrado"}, 404, {}

            if station_id and not ProjectModel.query.filter_by(id=project_id).first():
                return {"message": "Projeto inexistente"}, 404, {}

            if station_id and not StationModel.query.filter_by(id=station_id).first():
                return {"message": "Baliza inexistente"}, 404, {}

            coordinate = CoordinateModel.query.filter_by(
                projectID=project_id,
                userID=user_id,
                stationID=station_id,
                id=coordinate_id,
            ).all()

            response = {
                "coordinates": coordinate,
            }

            return response, 200, {}
        except:
            return {}
