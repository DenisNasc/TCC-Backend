from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from uuid import uuid4

from database.models.users import UserModel
from database.models.projects import ProjectModel
from database.models.stations import StationModel

from services.init_args import init_args

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
    "message": fields.String,
}


class StationsApi(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                return {"message": "Usuário não cadastrado"}, 404, {}

            if not ProjectModel.query.filter_by(id=project_id).first():
                return {"message": "Projeto inexistente"}, 404, {}

            stations = StationModel.query.filter_by(
                projectID=project_id, userID=user_id
            ).all()

            response = {
                "stations": stations,
                "userID": user_id,
                "projectID": project_id,
                "message": "Não há balizas para esse projeto",
            }

            return response, 200, {}

        except:
            return {"message": "Error inesperado no servidor"}, 500, {}

    @jwt_required()
    @marshal_with(response_fields)
    def post(self, user_id, project_id):
        try:
            fields = ("name", "longitudinal")

            args = init_args(fields)

            if not UserModel.query.filter_by(id=user_id).first():
                return {"message": "Usuário não cadastrado"}, 404, {}

            if not ProjectModel.query.filter_by(id=project_id).first():
                return {"message": "Projeto inexistente"}, 404, {}

            args["id"] = str(uuid4())
            args["userID"] = user_id
            args["projectID"] = project_id

            new_station = StationModel(**args)

            db.session.add(new_station)
            db.session.commit()

            stations = StationModel.query.filter_by(
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


class StationApi(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id, station_id):
        try:

            station = StationModel.query.filter_by(
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
