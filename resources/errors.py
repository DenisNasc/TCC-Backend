from werkzeug.exceptions import HTTPException


class InternalServerError(HTTPException):
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


errors = {
    "InternalServerError": {"message": "Erro inesperado no servidor", "status": 500},
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
}
