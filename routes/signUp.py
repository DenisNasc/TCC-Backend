import json
from flask import jsonify, request, g
from flask_jwt_extended import create_access_token, set_access_cookies

from uuid import uuid4
import bcrypt

from models.users import User

db = g.db
app = g.app


@app.route("/v1/signup", methods=["POST"])
def signUp():
    try:
        args = json.loads(request.data.decode("UTF-8").replace("'", '"'))

        email = User.query.filter_by(email=args["email"]).first()

        if email:
            return {"message": "Já existe um usuário com esse email"}, 409, {}

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(str.encode(args["password"]), salt)

        args["password"] = hashed.decode()
        args["id"] = str(uuid4())

        new_user = User(**args)

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=args["id"])

        response = {"message": "Usuário criado com sucesso!", "userID": args["id"]}
        response_JSON = jsonify(response)

        set_access_cookies(response_JSON, access_token)

        return response_JSON, 200, {}
    except:
        response = jsonify(
            {
                "message": "Erro inesperado no servidor",
            }
        )
        return response, 500, {}
