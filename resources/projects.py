from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from uuid import uuid4

from services.init_args import init_args

from database.models.projects import ProjectModel
from database.models.users import UserModel


from services.delOrParseFloat import delOrParseFloat

db = g.db

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
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id):
        try:
            projects = ProjectModel.query.filter_by(userID=user_id).all()

            response = {
                "projects": projects,
            }

            return response, 200, {}
        except:
            return {"message": "Erro inesperado no servidor!"}, 500, {}

    # @jwt_required()
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
                return {"message": "Usuário não existe"}, 400, {}

            name = ProjectModel.query.filter_by(name=args.name).first()

            if name:
                return {"message": "Ja existe um projeto com esse nome"}, 409, {}

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

            return response, 201, {}
        except:
            return {"message": "Erro inesperado no servidor!"}, 500, {}


class ProjectApi(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, project_id):
        try:

            project = ProjectModel.query.filter_by(
                userID=user_id, id=project_id
            ).first()

            response = {
                "projects": project,
            }

            return response, 200, {}
        except:
            return {"message": "Erro inesperado no servidor!"}, 500, {}

    @jwt_required()
    @marshal_with(response_fields)
    def put(self, user_id, project_id):
        return ""

    @jwt_required()
    @marshal_with(response_fields)
    def delete(self, user_id, project_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return {"message": "Este usuário não existe"}, 400, {}

            project = Project.query.filter_by(id=project_id).first()
            if not project:
                return {"message": "Este projeto não existe"}, 400, {}

            db.session.delete(project)
            db.session.commit()

            projects = Project.query.filter_by(userID=user_id).all()

            response = {
                "message": "Projeto deletado com sucesso!",
                "projects": projects,
            }

            return response, 200, {}
        except:
            return {"message": "Erro inesperado no servidor!"}, 500, {}
