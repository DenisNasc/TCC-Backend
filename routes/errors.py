from werkzeug.exceptions import HTTPException


class InternalServerError(HTTPException):
    pass


class RequestWithoutRequiredArgsError(HTTPException):
    pass


class EmailAlreadyExistsError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


# USER ERRORS
class UserNotFoundError(HTTPException):
    pass


class IncorrectCheckPasswordError(HTTPException):
    pass


# PROJECT ERRORS
class ProjectNotFoundError(HTTPException):
    pass


class ProjectAlreadyHasNameError(HTTPException):
    pass


# STATION ERRORS
class StationNotFoundError(HTTPException):
    pass


class StationAlreadyHasLongitudinalError(HTTPException):
    pass


class StationAlreadyHasNameError(HTTPException):
    pass


# COORDINATE ERRORS
class CoordinateNotFoundError(HTTPException):
    pass


errors = {
    "InternalServerError": {"message": "Erro inesperado no servidor", "status": 500},
    "RequestWithoutRequiredArgsError": {
        "message": "A requisição carece de argumentos obrigatórios",
        "status": 400,
    },
    "EmailAlreadyExistsError": {
        "message": "Usuário já cadastrado com esse email",
        "status": 400,
    },
    "UnauthorizedError": {"message": "Usuário ou senha incorretos", "status": 401},
    "UserNotFoundError": {
        "message": "Não existe um usuário com essas credênciais",
        "status": 401,
    },
    "IncorrectCheckPasswordError": {
        "message": "Confirmação de senha incorreta",
        "status": 401,
    },
    "ProjectNotFoundError": {
        "message": "Projeto inexistente",
        "status": 400,
    },
    "ProjectAlreadyHasNameError": {
        "message": "Um projeto já possui esse nome",
        "status": 400,
    },
    "StationNotFoundError": {
        "message": "Baliza inexistente",
        "status": 400,
    },
    "StationAlreadyHasLongitudinalError": {
        "message": "Uma baliza já possui essa posição longitudinal",
        "status": 400,
    },
    "StationAlreadyHasNameError": {
        "message": "Uma baliza já possui esse nome",
        "status": 400,
    },
    "CoordinateNotFoundError": {
        "message": "Coordenada inexistente",
        "status": 400,
    },
}
