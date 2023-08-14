from cores.exceptions import CustomResponse


class DecodeTokenException(CustomResponse):
    code = 400
    error_code = 10000
    message = "token decode error"


class ExpiredTokenException(CustomResponse):
    code = 400
    error_code = 10001
    message = "expired token"
