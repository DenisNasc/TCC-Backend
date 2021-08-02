from .auth import SignupApi
from .users import UsersApi, UserApi
from .projects import ProjectsApi, ProjectApi
from .stations import StationsApi, StationApi

from .coordinates import CoordinatesApi, CoordinateApi


def initialize_routes(api):
    api.add_resource(SignupApi, "/v1/signup")

    api.add_resource(UsersApi, "/v1/users")
    api.add_resource(UserApi, "/v1/users/<user_id>")

    api.add_resource(ProjectsApi, "/v1/users/<user_id>/projects")
    api.add_resource(ProjectApi, "/v1/users/<user_id>/projects/<project_id>")

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
