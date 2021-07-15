from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from models.users import User

from flask_jwt import jwt_required

from uuid import uuid4
import bcrypt

db = g.db

response_fields = {
    "id": fields.String,
    "uuid": fields.String,
    "username": fields.String,
    "password": fields.String,
    "email": fields.String,
    "createdAt": fields.DateTime,
    "updateddAt": fields.DateTime,
}


def init_args(fields):
    parser = reqparse.RequestParser()

    for field in fields:
        parser.add_argument(field)

    args = parser.parse_args()
    return args


class Users(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, uuid=0):
        try:
            if uuid == 0:
                users_all = User.query.all()
                return users_all, 200, {}

            user = User.query.filter_by(uuid=uuid).first()
            if not user:
                return {}, 400, {}

            return user, 200, {}
        except:
            return {}, 500, {}

    @marshal_with(response_fields)
    def post(self):
        fields = ("username", "email", "password")
        args = init_args(fields)

        try:
            username = User.query.filter_by(username=args.username).first()
            email = User.query.filter_by(username=args.email).first()

            if email or username:
                return {}, 409, {}

            user_uuid = str(uuid4())

            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(str.encode(args["password"]), salt)

            args["password"] = hashed.decode()

            new_user = User(uuid=user_uuid, **args)

            db.session.add(new_user)
            db.session.commit()

            return new_user, 201, {}

        except:
            return {}, 500, {}

    # @marshal_with(response_fields)
    def put(self, id):
        try:
            fields = ("username", "email", "password")
            args = init_args(fields)

            user = User.query.filter_by(id=id).first()

            if not user:
                response = {"message": "Não existe um usuário com esses dados"}

                return response, 400, {}

            user.username = args.username
            user.email = args.email
            user.password = args.password
            db.session.commit()

            response = {}

            return response, 204, {}
        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}

    # @marshal_with(response_fields)
    def delete(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if not user:
                response = {"message": "Este usuário não existe"}
                return response, 400, {}
            db.session.delete(user)
            db.session.commit()
        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}
