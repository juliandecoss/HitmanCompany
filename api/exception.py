from werkzeug.exceptions import HTTPException


class HitmanException(HTTPException):
    code = 403
    description = "Your password is incorrect or user does not exists"


class MissingParameterException(HTTPException):
    code = 400
    description = "Missing some parameters"


class ForbiddenException(HTTPException):
    code = 403
    description = "Your not authorized to access this resource"
