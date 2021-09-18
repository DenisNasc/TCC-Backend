from flask_restful import Api

from resources.auth import SignupApi
from resources.users import UsersApi, UserApi
from resources.projects import ProjectsApi, ProjectApi
from resources.stations import StationsApi, StationApi
from resources.coordinates import CoordinatesApi, CoordinateApi
from resources.hidrostatics import HidrostaticsApi


def initialize_routes(api: Api):
    api.add_resource(SignupApi, "/v1/signup")

    api.add_resource(UsersApi, "/v1/users")
    api.add_resource(UserApi, "/v1/users/<user_id>")

    api.add_resource(ProjectsApi, "/v1/users/<user_id>/projects")
    api.add_resource(ProjectApi, "/v1/users/<user_id>/projects/<project_id>")

    api.add_resource(
        HidrostaticsApi, "/v1/users/<user_id>/projects/<project_id>/hidrostatics"
    )

    api.add_resource(StationsApi, "/v1/users/<user_id>/projects/<project_id>/stations")
    api.add_resource(
        StationApi, "/v1/users/<user_id>/projects/<project_id>/stations/<station_id>"
    )

    api.add_resource(
        CoordinatesApi,
        "/v1/users/<user_id>/projects/<project_id>/stations/<station_id>/coordinates",
    )
    api.add_resource(
        CoordinateApi,
        "/v1/users/<user_id>/projects/<project_id>/stations/<station_id>/coordinates/<coordinate_id>",
    )
