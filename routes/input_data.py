from flask import g, send_from_directory
from flask_restful import Resource, reqparse, fields, marshal_with

from services.toExcel import input_data_to_excel

import pathlib

db = g.db

response_fields = {
    "data_converted": fields.String,
    "message": fields.String,
}


def init_args(fields):
    parser = reqparse.RequestParser()

    for field in fields:
        parser.add_argument(field)

    args = parser.parse_args()
    return args


class InputData(Resource):
    # @marshal_with(response_fields)
    def post(self):
        fields = [
            "data_raw",
        ]
        args = init_args(fields)

        import json

        olaaa = json.loads(args["data_raw"].replace("'", '"'))
        print(type(olaaa))

        try:
            file_name = input_data_to_excel(olaaa)

            # response = {"message": message}

            return send_from_directory(
                f"{pathlib.Path().absolute()}/static/sheets/",
                filename=file_name,
                as_attachment=True,
            )
            # return response, 200, {}

        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}
