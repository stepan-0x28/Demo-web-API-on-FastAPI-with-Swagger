import security
import models
import exceptions

from fastapi import Depends
from typing import AsyncGenerator, Annotated

from services.lock import Lock as LockService
from services.token import Token as TokenService
from services.data import Data as DataService
from database import AsyncSession

_lock_service = LockService()


def get_token_service() -> TokenService:
    return security.token_service


async def get_data_service() -> AsyncGenerator[DataService, None]:
    async with AsyncSession() as async_session:
        yield DataService(async_session)


async def get_current_user(token: Annotated[str, Depends(security.oauth2_scheme)],
                           token_service: Annotated[TokenService, Depends(get_token_service)],
                           data_service: Annotated[DataService, Depends(get_data_service)]) -> models.User:
    subject = token_service.get_subject(token)

    user = await data_service.user.get(subject['username'], subject['password'])

    if not user:
        raise exceptions.HTTPUnauthorizedException()

    return user


def get_lock_service() -> LockService:
    return _lock_service
