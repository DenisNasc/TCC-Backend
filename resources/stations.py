from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from uuid import uuid4

from database.models.users import UserModel
from database.models.projects import ProjectModel
from database.models.stations import StationModel
from database.models.coordinates import CoordinateModel

from services.init_args import init_args

from .errors import (
    InternalServerError,
    UserNotFoundError,
    ProjectNotFoundError,
    RequestWithoutRequiredArgsError,
    StationNotFoundError,
    StationAlreadyHasLongitudinalError,
    StationAlreadyHasNameError,
)

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
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            stations = StationModel.query.filter_by(
                projectID=project_id, userID=user_id
            ).all()

            response = {
                "stations": stations,
                "message": "",
            }

            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except:
            raise InternalServerError

    @jwt_required()
    @marshal_with(response_fields)
    def post(self, user_id, project_id):
        try:
            fields = ("name", "longitudinal")
            args = init_args(fields)

            if not args.name or not args.longitudinal:
                raise RequestWithoutRequiredArgsError

            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            if StationModel.query.filter_by(
                userID=user_id,
                projectID=project_id,
                longitudinal=args.longitudinal,
            ).first():
                raise StationAlreadyHasLongitudinalError

            if StationModel.query.filter_by(
                userID=user_id, projectID=project_id, name=args.name
            ).first():
                raise StationAlreadyHasNameError

            args["id"] = str(uuid4())
            args["userID"] = user_id
            args["projectID"] = project_id

            new_station = StationModel(**args)

            db.session.add(new_station)
            db.session.commit()

            response = {
                "stations": new_station,
                "message": "Baliza criada com sucesso!",
            }

            return response, 201
        except RequestWithoutRequiredArgsError:
            raise RequestWithoutRequiredArgsError
        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except StationAlreadyHasLongitudinalError:
            raise StationAlreadyHasLongitudinalError
        except StationAlreadyHasNameError:
            raise StationAlreadyHasNameError
        except:
            raise InternalServerError


class StationApi(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id, station_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            station = StationModel.query.filter_by(
                projectID=project_id, userID=user_id, id=station_id
            ).first()

            if not station:
                raise StationNotFoundError

            response = {"stations": station, "message": ""}

            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except StationNotFoundError:
            raise StationNotFoundError
        except:
            raise InternalServerError

    def put(self, user_id, project_id, station_id):
        try:
            fields = ("name", "longitudinal")
            args = init_args(fields)

            station = StationModel.query.filter_by(
                projectID=project_id, userID=user_id, id=station_id
            ).first()

            if not station:
                raise StationNotFoundError

            station.name = args.name
            station.longitudinal = args.longitudinal

            db.session.commit()

            response = {
                "message": "Baliza atualizada com sucesso!",
                "stations": station,
            }

            return response, 200

        except StationNotFoundError:
            raise StationNotFoundError
        except:
            raise InternalServerError

    def delete(self, user_id, project_id, station_id):
        try:
            station = StationModel.query.filter_by(
                projectID=project_id, userID=user_id, id=station_id
            ).first()

            if not station:
                raise StationNotFoundError

            CoordinateModel.query.filter(
                CoordinateModel.stationID == station_id
            ).delete()

            db.session.delete(station)
            print(station)
            db.session.commit()

            response = {"message": "Baliza deletada com sucesso!"}
            return response, 200

        except StationNotFoundError:
            raise StationNotFoundError
