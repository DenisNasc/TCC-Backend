from flask_restful import reqparse


def init_args(fields):
    parser = reqparse.RequestParser()

    for field in fields:
        parser.add_argument(field)

    args = parser.parse_args()
    return args
