from flask import g, jsonify
from flask_jwt_extended import unset_jwt_cookies

app = g.app


@app.route("/v1/logout", methods=["POST"])
def logout():
    try:
        response = jsonify(
            {
                "message": "Logout efetuado com sucesso!",
            }
        )
        unset_jwt_cookies(response)
        return response
    except:
        response = jsonify(
            {
                "message": "Erro inesperado no servidor",
            }
        )
        return response, 500, {}
