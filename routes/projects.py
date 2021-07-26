from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt import jwt_required

from models.projects import Project
from models.users import User

from uuid import uuid4

from services.delOrParseFloat import delOrParseFloat

db = g.db

response_fields = {
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


def init_args(fields):
    parser = reqparse.RequestParser()

    for field in fields:
        parser.add_argument(field)

    args = parser.parse_args()
    return args


class Projects(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id, id=None):
        try:
            if not id:
                projects = Project.query.filter_by(userID=user_id).all()

                return projects, 200, {}

            project = Project.query.filter_by(userID=user_id, id=id).first()

            return project, 200, {}
        except:
            return {}, 500, {}

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

            user = User.query.filter_by(id=user_id).first()

            if not user:
                response = {"message": "Usuário não existe"}

                return response, 400, {}

            name = Project.query.filter_by(name=args.name).first()

            if name:
                response = {"message": "Ja existe um projeto com esse nome"}

                return response, 409, {}

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

            new_project = Project(**args)

            db.session.add(new_project)
            db.session.commit()

            return new_project, 201, {}
        except:
            return {}, 500, {}

    @jwt_required()
    @marshal_with(response_fields)
    def delete(self, user_id, id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return {}, 400, {}

            project = Project.query.filter_by(id=id).first()
            if not project:
                return {}, 400, {}

            db.session.delete(project)
            db.session.commit()

            return {}, 200, {}
        except:
            return {}, 500, {}
