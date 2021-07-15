from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from models.users import User
from models.projects import Project
from models.stations import Station

db = g.db

response_fields = {
    "name": fields.String,
    "id": fields.String,
    "user_id": fields.String,
    "error_message": fields.String,
}


class Stations(Resource):
    @marshal_with(response_fields)
    def get(self):
        return {}, 200, {}