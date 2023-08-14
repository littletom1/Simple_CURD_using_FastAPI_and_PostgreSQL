from http import HTTPStatus
from fastapi.responses import JSONResponse

class CustomResponse(JSONResponse):
    status_code = HTTPStatus.BAD_GATEWAY
    content = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, content=None, status_code=200) -> None:
        if content:
            self.content = content
            self.status_code = status_code
        super().__init__(self.content, self.status_code)


class BadRequestResponse(CustomResponse):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    content = HTTPStatus.BAD_REQUEST.description


class NotFoundResponse(CustomResponse):
    status_code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    content = HTTPStatus.NOT_FOUND.description


class ForbiddenResponse(CustomResponse):
    status_code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    content = HTTPStatus.FORBIDDEN.description


class UnauthorizedResponse(CustomResponse):
    status_code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    content = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomResponse):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    content = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueResponse(CustomResponse):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    content = 'Object already exists'
