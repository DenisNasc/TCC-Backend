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

hidrostatic_fields = {
    "draft": fields.Float,
    "volume": fields.Float,
    "displacement": fields.Float,
    "LCB": fields.Float,
    "VCB": fields.Float,
    "KMT": fields.Float,
    "MT1": fields.Float,
    "LCF": fields.Float,
    "CB": fields.Float,
    "CP": fields.Float,
    "wetedSurface": fields.Float,
}

response_fields = {
    "hidrostatics": fields.List(fields.Nested(hidrostatic_fields)),
    "drafts": fields.List(fields.Float),
}


class HidrostaticsApi(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.DRAFTS = []
        self.STATIONS = []
        self.HIDROSTATICS = {"volumes": []}

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

    def _calculate_stations_area(self, draft):
        for key, station in enumerate(self.STATIONS):
            coordinates = station["coordinates"]

            area = stationArea(coordinates, draft)

            self.STATIONS[key]["areas"].append({"area": area, "draft": draft})

    def _calculate_volume(self, draft):
        longitudinals = [x["longitudinal"] for x in self.STATIONS]
        areas = [station["areas"] for station in self.STATIONS]

        areasFormated = []

        for value in areas:
            for area in value:
                if area["draft"] == draft:
                    areasFormated.append(area["area"])

        volume = round(integrate.simpson(y=areasFormated, x=longitudinals), 4)
        self.HIDROSTATICS["volumes"].append({"volume": volume, "draft": draft})

    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id):
        try:
            if not UserModel.query.filter_by(id=user_id).first():
                raise UserNotFoundError

            if not ProjectModel.query.filter_by(id=project_id).first():
                raise ProjectNotFoundError

            project = ProjectModel.query.filter_by(id=project_id).first()

            self.DRAFTS = [
                round(x, 4) for x in np.arange(1, project.draft + 0.05, 0.05)
            ]

            stations = (
                StationModel.query.filter_by(projectID=project_id)
                .order_by(StationModel.longitudinal)
                .all()
            )

            self._format_data(stations)

            for draft in self.DRAFTS:
                self._calculate_stations_area(draft)

            for draft in self.DRAFTS:
                self._calculate_volume(draft)

            # print(self.HIDROSTATICS["volumes"])
            hidrostatics = []

            for key, draft in enumerate(self.DRAFTS):
                volume = self.HIDROSTATICS["volumes"][key]["volume"]
                print(volume)

                hidrostatics.append({"draft": draft, "volume": volume})

            return {
                "drafts": self.DRAFTS,
                "hidrostatics": hidrostatics,
            }, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except:
            raise InternalServerError
