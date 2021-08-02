from werkzeug.exceptions import HTTPException


class InternalServerError(HTTPException):
    pass


class EmailAlreadyExistsError(HTTPException):
    pass


class UnauthorizedError(HTTPException):
    pass


errors = {
    "InternalServerError": {"message": "Erro inesperado no servidor", "status": 500},
    "EmailAlreadyExistsError": {
        "message": "Usuário já cadastrado com esse email",
        "status": 400,
    },
    "UnauthorizedError": {"message": "Usuário ou senha incorretos", "status": 401},
}
