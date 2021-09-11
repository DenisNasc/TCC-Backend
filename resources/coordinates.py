from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from uuid import uuid4

from services.init_args import init_args

from database.models.users import UserModel
from database.models.projects import ProjectModel
from database.models.stations import StationModel
from database.models.coordinates import CoordinateModel

from .errors import (
    InternalServerError,
    ProjectNotFoundError,
    StationNotFoundError,
    UserNotFoundError,
    CoordinateNotFoundError,
)

db = g.db

coordinates_fields = {
    "id": fields.String,
    "stationID": fields.String,
    "type": fields.String,
    "vertical": fields.Float,
    "transversal": fields.Float,
    "createdAt": fields.DateTime,
    "updatedAt": fields.DateTime,
}

response_fields = {
    "coordinates": fields.List(fields.Nested(coordinates_fields)),
    "userID": fields.String,
    "projectID": fields.String,
    "stationID": fields.String,
    "message": fields.String,
}


class CoordinatesApi(Resource):
    def _verify_request(self, user_id, project_id, station_id):
        if not UserModel.query.filter_by(id=user_id).first():
            raise UserNotFoundError

        if not ProjectModel.query.filter_by(id=project_id).first():
            raise ProjectNotFoundError

        if not StationModel.query.filter_by(id=station_id).first():
            raise StationNotFoundError

    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id, station_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            if not StationModel.query.filter_by(id=station_id).first():
                raise StationNotFoundError

            coordinates = CoordinateModel.query.filter_by(
                userID=user_id, projectID=project_id, stationID=station_id
            ).all()

            response = {
                "message": "",
                "coordinates": coordinates,
            }

            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except StationNotFoundError:
            raise StationNotFoundError
        except:
            raise InternalServerError

    @jwt_required()
    @marshal_with(response_fields)
    def post(self, user_id, project_id, station_id):
        try:
            fields = ("type", "vertical", "transversal")

            args = init_args(fields)

            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            if not StationModel.query.filter_by(id=station_id).first():
                raise StationNotFoundError

            args["id"] = str(uuid4())
            args["userID"] = user_id
            args["projectID"] = project_id
            args["stationID"] = station_id

            new_coordinate = CoordinateModel(**args)

            db.session.add(new_coordinate)
            db.session.commit()

            coordinates = CoordinateModel.query.filter_by(
                userID=user_id, projectID=project_id, stationID=station_id
            ).all()

            response = {
                "coordinates": coordinates,
                "message": "Coordenada criada com sucesso!",
            }

            return response, 201

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except StationNotFoundError:
            raise StationNotFoundError
        except:
            raise InternalServerError


class CoordinateApi(Resource):
    def get(self, user_id, project_id, station_id, coordinate_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            if not StationModel.query.filter_by(id=station_id).first():
                raise StationNotFoundError

            coordinate = CoordinateModel.query.filter_by(id=coordinate_id).first()

            if not coordinate:
                raise CoordinateNotFoundError

            response = {"coordinates": coordinate}

            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except StationNotFoundError:
            raise StationNotFoundError
        except CoordinateNotFoundError:
            raise CoordinateNotFoundError

        except:
            raise InternalServerError

    def put(self, user_id, project_id, station_id, coordinate_id):
        try:
            fields = ("name", "longitudinal")
            args = init_args(fields)

            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            if not StationModel.query.filter_by(id=station_id).first():
                raise StationNotFoundError

            coordinate = CoordinateModel.query.filter_by(id=coordinate_id).first()

            if not coordinate:
                raise CoordinateNotFoundError

            for key, value in args.items():
                if value:
                    coordinate[key] = value

            db.session.commit()

            response = {
                "message": "Baliza atualizada com sucesso!",
                "coordinates": coordinate,
            }

            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except StationNotFoundError:
            raise StationNotFoundError
        except CoordinateNotFoundError:
            raise CoordinateNotFoundError

        except:
            raise InternalServerError

    def delete(self, user_id, project_id, station_id, coordinate_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            if not StationModel.query.filter_by(id=station_id).first():
                raise StationNotFoundError

            coordinate = CoordinateModel.query.filter_by(id=coordinate_id).first()

            db.session.delete(coordinate)
            db.session.commit()

            response = {
                "message": "Coordenada deletada com sucesso!",
            }
            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except StationNotFoundError:
            raise StationNotFoundError
        except CoordinateNotFoundError:
            raise CoordinateNotFoundError
        except:
            raise InternalServerError
