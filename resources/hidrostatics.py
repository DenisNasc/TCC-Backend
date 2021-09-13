from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from scipy import integrate
import numpy as np

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
    def __init__(self) -> None:
        super().__init__()
        self.DRAFTS = []
        self.STATIONS = []
        self.HIDROSTATICS = {}

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
                {
                    "vertical": x["vertical"],
                    "transversal": x["transversal"],
                    "type": x["type"],
                }
                for x in coordinates
            ]

            station["coordinates"] = coordinates
            station["areas"] = []

            del station["_sa_instance_state"]
            del station["userID"]
            del station["projectID"]
            del station["createdAt"]
            del station["updatedAt"]

            stations[key] = station

        self.STATIONS = stations

    def _calculate_area(self, draft):
        for key, station in enumerate(self.STATIONS):
            coordinates = station["coordinates"]

            area = stationArea(coordinates, draft)

            self.STATIONS[key]["areas"].append({"area": area, "draft": round(draft, 4)})

    def _calculate_moldade_volume(self, draft):
        areas = [x["area"] for x in self.STATIONS]
        longitudinals = [x["longitudinal"] for x in self.STATIONS]

        volume = integrate.simpson(y=areas, x=longitudinals)

        self.HIDROSTATICS["MOLDADE_VOLUME"] = volume

    def get(self, user_id, project_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            project = ProjectModel.query.filter_by(id=project_id).first()

            self.DRAFTS = np.arange(1, project.draft + 0.05, 0.05)

            stations = (
                StationModel.query.filter_by(projectID=project_id)
                .order_by(StationModel.longitudinal)
                .all()
            )

            self._format_data(stations)

            for draft in self.DRAFTS:
                self._calculate_area(draft)

            print(self.STATIONS)

            return {"hidrostatics": self.HIDROSTATICS}, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except:
            raise InternalServerError
