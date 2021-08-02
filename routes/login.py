import json
from flask import jsonify, request, g
from flask_jwt_extended import create_access_token, set_access_cookies
import bcrypt


from models.users import User

app = g.app


@app.route("/v1/login", methods=["POST"])
def login():
    try:
        args = json.loads(request.data.decode("UTF-8").replace("'", '"'))

        email = args["email"]
        password = args["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "Usuário não cadastrado"}, 400

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return {"message": "Senha incorreta"}, 400

        access_token = create_access_token(identity=user.id)

        response = {"message": "Login efetuado com sucesso!", "userID": user.id}

        response_JSON = jsonify(response)
        set_access_cookies(response_JSON, access_token)

        return response_JSON, 200, {}
    except:
        response = {
            "message": "Erro inesperado no servidor",
        }
        return response, 500, {}
