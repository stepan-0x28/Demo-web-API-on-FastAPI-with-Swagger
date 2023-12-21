import schemas
import dependencies
import exceptions

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from services.data import Data as DataService
from services.token import Token as TokenService

router = APIRouter(prefix='/token', tags=['token'])


@router.post('', response_model=schemas.Token)
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       data_service: Annotated[DataService, Depends(dependencies.get_data_service)],
                       token_service: Annotated[TokenService, Depends(dependencies.get_token_service)]):
    user = await data_service.users.get_one(form_data.username, form_data.password)

    if not user:
        raise exceptions.HTTPUnauthorizedException()

    token = token_service.create({'username': user.username, 'password': user.password})

    return schemas.Token(access_token=token)
