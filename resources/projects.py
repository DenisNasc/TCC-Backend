from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from uuid import uuid4

from services.init_args import init_args
from services.stationArea import stationArea

from models.users import UserModel
from models.projects import ProjectModel


from routes.errors import (
    InternalServerError,
    ProjectNotFoundError,
    UserNotFoundError,
    ProjectAlreadyHasNameError,
)

from services.delOrParseFloat import delOrParseFloat


project_fields = {
    "id": fields.String,
    "userID": fields.String,
    "name": fields.String,
    "engineer": fields.String,
    "shipyard": fields.String,
    "lengthOverall": fields.Float,
    "lengthPerpendiculars": fields.Float,
    "breadth": fields.Float,
    "draft": fields.Float,
    "createdAt": fields.DateTime,
    "updateddAt": fields.DateTime,
}

response_fields = {
    "projects": fields.List(fields.Nested(project_fields)),
    "message": fields.String,
}


class ProjectsApi(Resource):
    # @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id):
        try:
            user = UserModel.query.filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError

            projects = ProjectModel.query.filter_by(userID=user_id).all()

            response = {
                "message": "",
                "projects": projects,
            }

            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except:
            raise InternalServerError

    @jwt_required()
    @marshal_with(response_fields)
    def post(self, user_id):
        try:
            fields = (
                "name",
                "lengthOverall",
                "lengthPerpendiculars",
                "breadth",
                "draft",
                "engineer",
                "shipyard",
            )
            args = init_args(fields)

            user = UserModel.query.filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError

            name = ProjectModel.query.filter_by(userID=user_id, name=args.name).first()

            if name:
                raise ProjectAlreadyHasNameError

            if not args["engineer"]:
                args["engineer"] = user.name

            if not args["shipyard"]:
                del args["shipyard"]

            delOrParseFloat(args, "lengthOverall")
            delOrParseFloat(args, "lengthPerpendiculars")
            delOrParseFloat(args, "breadth")
            delOrParseFloat(args, "draft")

            args["id"] = str(uuid4())
            args["userID"] = user_id

            new_project = ProjectModel(**args)

            db.session.add(new_project)
            db.session.commit()

            response = {
                "message": "Projeto criado com sucesso!",
                "projects": new_project,
            }

            return response, 201

        except UserNotFoundError:
            raise UserNotFoundError
        except ProjectAlreadyHasNameError:
            raise ProjectAlreadyHasNameError
        except:
            raise InternalServerError


class ProjectApi(Resource):
    # @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id):
        try:
            project = ProjectModel.query.filter_by(
                userID=user_id, id=project_id
            ).first()

            response = {
                "message": "",
                "projects": project,
            }

            return response, 200

        except:
            raise InternalServerError

    @jwt_required()
    @marshal_with(response_fields)
    def put(self, user_id, project_id):
        try:
            fields = (
                "name",
                "lengthOverall",
                "lengthPerpendiculars",
                "breadth",
                "draft",
                "engineer",
                "shipyard",
            )
            args = init_args(fields)

            project = ProjectModel.query.filter_by(
                userID=user_id, id=project_id
            ).first()

            if not project:
                raise ProjectNotFoundError

            for key, value in args.items():
                if not value:
                    pass
                else:
                    project[key] = value

        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except:
            raise InternalServerError

    @jwt_required()
    @marshal_with(response_fields)
    def delete(self, user_id, project_id):
        try:
            user = UserModel.query.filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError

            project = ProjectModel.query.filter_by(
                userID=user_id, id=project_id
            ).first()

            if not project:
                raise ProjectNotFoundError

            db.session.delete(project)
            db.session.commit()

            projects = ProjectModel.query.filter_by(userID=user_id).all()

            response = {
                "message": "Projeto deletado com sucesso!",
                "projects": projects,
            }

            return response, 200

        except ProjectNotFoundError:
            raise ProjectNotFoundError
        except:
            raise InternalServerError
