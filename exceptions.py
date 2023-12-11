from fastapi import HTTPException, status


class HTTPUnauthorizedException(HTTPException):
    def __init__(self):
        super(HTTPUnauthorizedException, self).__init__(status.HTTP_401_UNAUTHORIZED,
                                                        'Incorrect username or password',
                                                        {'WWW-Authenticate': 'Bearer'})
