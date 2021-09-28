from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from scipy import integrate
import numpy as np

from services.hidrostatics.calculateStationArea import calculateStationArea
from services.hidrostatics.calculateVolume import calculateVolume
from services.hidrostatics.calculateWaterlineArea import calculateWaterlineArea
from services.hidrostatics.calculateVCB import calculateVCB
from services.hidrostatics.calculateLCF import calculateLCF
from services.hidrostatics.calculateBM import calculateBM
from services.hidrostatics.calculateMT1 import calculateMT1

from models.users import UserModel
from models.projects import ProjectModel
from models.stations import StationModel
from models.coordinates import CoordinateModel


from routes.errors import (
    InternalServerError,
    ProjectNotFoundError,
    UserNotFoundError,
)


hidrostatic_fields = {
    "draft": fields.Float,
    "volume": fields.Float,
    "displacement": fields.Float,
    "AWL": fields.Float,
    "LCB": fields.Float,
    "VCB": fields.Float,
    "BM": fields.Float,
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
        self.LPP = 0
        self.LONGITUDINALS = []
        self.DRAFTS = []
        self.STATIONS = []
        self.HIDROSTATICS = {
            "volumes": [],
            "displacements": [],
            "LCBs": [],
            "AWLs": [],
            "VCBs": [],
            "LCFs": [],
            "BMs": [],
            "MT1s": [],
        }

    def generateDrafts(self, maxDraft: float):
        self.DRAFTS = [round(x, 4) for x in np.arange(0.05, maxDraft + 0.05, 0.05)]

    def handleStationsData(self, stationsDB: list):
        stations = [
            {
                "longitudinal": station.longitudinal,
                "coordinates": station.coordinates,
                "areas": [],
            }
            for station in stationsDB
        ]

        self.STATIONS = stations
        self.LONGITUDINALS = [x["longitudinal"] for x in self.STATIONS]

    def calculateStationsArea(self, draft: float):
        for key, station in enumerate(self.STATIONS):
            coordinates = station["coordinates"]

            area = calculateStationArea(coordinates, draft)

            self.STATIONS[key]["areas"].append({"area": area, "draft": draft})

    def calculateShipVolume(self, draft):
        longitudinals = self.LONGITUDINALS
        areas = [station["areas"] for station in self.STATIONS]

        areasFormated = []

        for value in areas:
            for area in value:
                if area["draft"] == draft:
                    areasFormated.append(area["area"])

        volume = calculateVolume(longitudinals, areasFormated)

        self.HIDROSTATICS["volumes"].append({"volume": volume, "draft": draft})

    def calculateShipDisplacement(self, key, draft):
        volume = self.HIDROSTATICS["volumes"][key]
        if volume["draft"] == draft:
            self.HIDROSTATICS["displacements"].append(
                {"draft": draft, "displacement": round(volume["volume"] * 1.025, 4)}
            )

    def calculateShipLCB(self, key, draft):
        longitudinals = self.LONGITUDINALS
        volumes = self.HIDROSTATICS["volumes"][key]
        volume = 0

        if volumes["draft"] == draft:
            volume = volumes["volume"]

        areasForLCB = []
        for station in self.STATIONS:

            areas = station["areas"]
            for area in areas:
                if area["draft"] == draft:
                    areasForLCB.append(area["area"])

        moments = []
        for key, long in enumerate(longitudinals):
            moments.append(areasForLCB[key] * long)

        LCB = round(integrate.simpson(y=moments, x=longitudinals) / volume, 4)

        self.HIDROSTATICS["LCBs"].append({"draft": draft, "LCB": LCB})

    def calculateShipAWL(self, draft):
        waterlineArea = calculateWaterlineArea(self.LONGITUDINALS, self.STATIONS, draft)

        self.HIDROSTATICS["AWLs"].append({"AWL": waterlineArea, "draft": draft})

    def calculateShipVCB(self, key, draft):
        drafts = self.DRAFTS[0 : key + 1]
        AWLs = [value["AWL"] for value in self.HIDROSTATICS["AWLs"][0 : key + 1]]
        volume = self.HIDROSTATICS["volumes"][key]["volume"]
        VCB = calculateVCB(drafts, AWLs, volume)

        self.HIDROSTATICS["VCBs"].append({"draft": draft, "VCB": VCB})

    def calculateShipLCF(self, key, draft):
        AWL = self.HIDROSTATICS["AWLs"][key]["AWL"]
        LCF = calculateLCF(self.LONGITUDINALS, self.STATIONS, draft, AWL)

        self.HIDROSTATICS["LCFs"].append({"LCF": LCF, "draft": draft})

    def calculateShipBM(self, key, draft):
        volume = self.HIDROSTATICS["volumes"][key]["volume"]
        BM = calculateBM(self.LONGITUDINALS, self.STATIONS, draft, volume)

        self.HIDROSTATICS["BMs"].append({"BM": BM, "draft": draft})

    def calculateShipMT1(self, key, draft):
        displacement = self.HIDROSTATICS["displacements"][key]["displacement"]
        MT1 = calculateMT1(displacement, 1, self.LPP)

        self.HIDROSTATICS["MT1s"].append({"MT1": MT1, "draft": draft})

    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id):

        if not UserModel.query.filter_by(id=user_id).first():
            raise UserNotFoundError

        project = ProjectModel.query.filter_by(id=project_id).first()
        if not project:
            raise ProjectNotFoundError

        stations = (
            StationModel.query.filter_by(projectID=project_id)
            .order_by(StationModel.longitudinal)
            .all()
        )
        self.LPP = project.lengthPerpendiculars
        maxDraft = project.depth

        self.generateDrafts(maxDraft)
        self.handleStationsData(stations)

        for draft in self.DRAFTS:
            self.calculateStationsArea(draft)

        for key, draft in enumerate(self.DRAFTS):
            self.calculateShipVolume(draft)
            self.calculateShipDisplacement(key, draft)
            self.calculateShipLCB(key, draft)
            self.calculateShipAWL(draft)
            self.calculateShipVCB(key, draft)
            self.calculateShipLCF(key, draft)
            self.calculateShipBM(key, draft)
            self.calculateShipMT1(key, draft)

        hidrostatics = []

        for key, draft in enumerate(self.DRAFTS):
            volume = self.HIDROSTATICS["volumes"][key]["volume"]
            displacement = self.HIDROSTATICS["displacements"][key]["displacement"]
            LCB = self.HIDROSTATICS["LCBs"][key]["LCB"]
            AWL = self.HIDROSTATICS["AWLs"][key]["AWL"]
            VCB = self.HIDROSTATICS["VCBs"][key]["VCB"]
            LCF = self.HIDROSTATICS["LCFs"][key]["LCF"]
            BM = self.HIDROSTATICS["BMs"][key]["BM"]
            MT1 = self.HIDROSTATICS["MT1s"][key]["MT1"]
            # ADD AS OUTRAS HIDROSTATICAS AQUI

            hidrostatics.append(
                {
                    "draft": draft,
                    "volume": volume,
                    "displacement": displacement,
                    "LCB": LCB,
                    "AWL": AWL,
                    "VCB": VCB,
                    "LCF": LCF,
                    "BM": BM,
                    "MT1": MT1,
                }
            )

        return {
            "drafts": self.DRAFTS,
            "hidrostatics": hidrostatics,
        }, 200
