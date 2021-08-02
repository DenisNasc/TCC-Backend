from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required

from uuid import uuid4


from services.init_args import init_args

from database.models.users import UserModel

db = g.db

user_fields = {
    "id": fields.String,
    "name": fields.String,
    "password": fields.String,
    "email": fields.String,
    "createdAt": fields.DateTime,
    "updateddAt": fields.DateTime,
}


response_fields = {
    "users": fields.List(fields.Nested(user_fields)),
    "message": fields.String,
}


class UserApi(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self, user_id):
        try:
            user = UserModel.query.filter_by(id=user_id).all()
            if not user:
                return {"message": "Usuário não cadastrado"}, 400, {}

            response = {"users": user}
            return response, 200, {}
        except:
            return {"message": "Erro inesperado no servidor"}, 500, {}

    @jwt_required()
    @marshal_with(response_fields)
    def put(self, user_id):
        try:
            fields = ("name", "email", "password")
            args = init_args(fields)

            user = UserModel.query.filter_by(id=user_id).first()

            if not user:
                response = {"message": "Não existe um usuário com esses dados"}

                return response, 400, {}

            user.name = args.name
            user.email = args.email
            user.password = args.password

            db.session.commit()

            response = {}

            return response, 204, {}
        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}

    @jwt_required()
    @marshal_with(response_fields)
    def delete(self, user_id):
        try:
            user = UserModel.query.filter_by(id=user_id).first()

            if not user:
                response = {"message": "Este usuário não existe"}
                return response, 400, {}

            db.session.delete(user)
            db.session.commit()

            response = {"message": "Usuário deletado com sucesso!"}
            return response, 200, {}

        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}


class UsersApi(Resource):
    # @jwt_required()
    @marshal_with(response_fields)
    def get(self):
        try:
            users = UserModel.query.filter_by().all()

            response = {"users": users}
            return response, 200, {}
        except:
            return {"message": "Erro inesperado no servidor"}, 500, {}
