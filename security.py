import services

from fastapi.security import OAuth2PasswordBearer
from os import environ

oauth2_scheme = OAuth2PasswordBearer('token')

token_service = services.Token(environ.get('ENCRYPTION_KEY'))
