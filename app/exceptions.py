class JWTException(Exception):
    pass


class JWTNoPublicKey(JWTException):
    pass


class JWTUsernameNotFound(JWTException):
    pass
