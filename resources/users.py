from flask import g
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required


from services.init_args import init_args

from database.models.users import UserModel

from .errors import (
    IncorrectCheckPasswordError,
    UserNotFoundError,
    InternalServerError,
    EmailAlreadyExistsError,
)

db = g.db

user_fields = {
    "id": fields.String,
    "name": fields.String,
    "password": fields.String,
    "email": fields.String,
    "createdAt": fields.DateTime,
    "updatedAt": fields.DateTime,
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
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                raise UserNotFoundError

            response = {"users": user}
            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except:
            raise InternalServerError

    @jwt_required()
    @marshal_with(response_fields)
    def put(self, user_id):
        try:
            fields = ("name", "email", "password", "checkPassword")
            args = init_args(fields)

            user = UserModel.query.filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError

            if not user.check_password(args.checkPassword):
                raise IncorrectCheckPasswordError

            if args.name:
                user.name = args.name

            if args.email:
                if UserModel.query.filter_by(email=args.email).first():
                    raise EmailAlreadyExistsError

                user.email = args.email

            if args.password:
                user.password = args.password
                user.hash_password()

            db.session.commit()

            response = {
                "message": "Usuário atualizado com sucesso!",
                "users": user,
            }

            return response, 200
        except UserNotFoundError:
            raise UserNotFoundError
        except IncorrectCheckPasswordError:
            raise IncorrectCheckPasswordError
        except EmailAlreadyExistsError:
            raise EmailAlreadyExistsError
        except:
            raise InternalServerError

    @jwt_required()
    @marshal_with(response_fields)
    def delete(self, user_id):
        try:
            fields = ("checkPassword",)
            args = init_args(fields)

            user = UserModel.query.filter_by(id=user_id).first()

            if not user:
                raise UserNotFoundError

            if not user.check_password(args.checkPassword):
                raise IncorrectCheckPasswordError

            db.session.delete(user)
            db.session.commit()

            response = {"message": "Usuário deletado com sucesso!", "users": user}
            return response, 200

        except UserNotFoundError:
            raise UserNotFoundError
        except IncorrectCheckPasswordError:
            raise IncorrectCheckPasswordError
        except:
            raise InternalServerError


class UsersApi(Resource):
    @jwt_required()
    @marshal_with(response_fields)
    def get(self):
        try:
            users = UserModel.query.filter_by().all()

            response = {"users": users}
            return response, 200

        except:
            raise InternalServerError
