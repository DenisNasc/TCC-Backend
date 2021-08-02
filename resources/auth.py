import json
from flask import g, request, jsonify
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import (
    set_access_cookies,
    create_access_token,
    unset_jwt_cookies,
)


from resources.errors import (
    InternalServerError,
    EmailAlreadyExistsError,
)
from database.models.users import UserModel

from uuid import uuid4
from services.init_args import init_args


db = g.db

response_fields = {"message": fields.String, "userID": fields.String}


class SignupApi(Resource):
    @marshal_with(response_fields)
    def post(self):
        try:
            params = ("name", "email", "password")
            args = init_args(params)
            args["id"] = str(uuid4())

            if UserModel.query.filter_by(email=args.email).first():
                raise EmailAlreadyExistsError

            user = UserModel(**args)
            user.hash_password()

            db.session.add(user)
            db.session.commit()

            response = {"message": "", "userID": str(user.id)}
            return response, 200

        except EmailAlreadyExistsError:
            raise EmailAlreadyExistsError

        except:
            raise InternalServerError


def initialize_auth_routes(app):
    @app.route("/v1/login", methods=["POST"])
    def login():
        try:
            params = request.data.decode("UTF-8")
            args = json.loads(params)

            user = UserModel.query.filter_by(email=args["email"]).first()

            if not user or not user.check_password(args["password"]):
                return {"message": "Email ou senha incorretos"}, 401

            access_token = create_access_token(identity=user.id)

            response = jsonify({"message": "Login realizado com sucesso!"})

            access_token = create_access_token(identity="example_user")
            set_access_cookies(response, access_token)

            return response, 200

        except:
            return {"message": "Erro inesperado no servidor"}, 500

    @app.route("/v1/logout", methods=["POST"])
    def logout():
        try:
            response = jsonify({"message": "Logout realizado com sucesso!"})
            unset_jwt_cookies(response)

            return response, 200

        except:
            return {"message": "Erro inesperado no servidor"}, 500
