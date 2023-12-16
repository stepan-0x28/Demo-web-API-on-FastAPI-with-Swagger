from fastapi import HTTPException, status


class HTTPUnauthorizedException(HTTPException):
    def __init__(self):
        super(HTTPUnauthorizedException, self).__init__(status.HTTP_401_UNAUTHORIZED,
                                                        'Incorrect username or password',
                                                        {'WWW-Authenticate': 'Bearer'})


class HTTPForbiddenException(HTTPException):
    def __init__(self):
        super(HTTPForbiddenException, self).__init__(status.HTTP_403_FORBIDDEN,
                                                     'Forbidden (based on user role)')
