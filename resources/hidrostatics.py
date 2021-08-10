from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required


from services.stationArea import stationArea

from database.models.users import UserModel
from database.models.projects import ProjectModel
from database.models.stations import StationModel
from database.models.coordinates import CoordinateModel


from .errors import (
    InternalServerError,
    ProjectNotFoundError,
    UserNotFoundError,
)


db = g.db


class HidrostaticsApi(Resource):
    def _format_data(self, stations):
        stations = [x.__dict__ for x in stations]

        for key, station in enumerate(stations):
            coordinates = (
                CoordinateModel.query.filter_by(stationID=station["id"])
                .order_by(CoordinateModel.order)
                .all()
            )

            coordinates = [x.__dict__ for x in coordinates]
            coordinates = [
                {"vertical": x["vertical"], "transversal": x["transversal"]}
                for x in coordinates
            ]

            station["coordinates"] = coordinates

            del station["_sa_instance_state"]
            del station["userID"]
            del station["projectID"]
            del station["createdAt"]
            del station["updatedAt"]

            stations[key] = station

        for key, station in enumerate(stations):
            coordinates = station["coordinates"]

            area = stationArea(coordinates)
            station["area"] = area
            stations[key] = station

        self.STATIONS = stations

    def get(self, user_id, project_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            stations = (
                StationModel.query.filter_by(projectID=project_id)
                .order_by(StationModel.longitudinal)
                .all()
            )

            self._format_data(stations)

            print(self.STATIONS)

            return {}, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except:
            raise InternalServerError
