from fastapi.security import OAuth2PasswordBearer
from os import environ

from services.token import Token as TokenService

oauth2_scheme = OAuth2PasswordBearer('token')

token_service = TokenService(environ.get('ENCRYPTION_KEY'))
