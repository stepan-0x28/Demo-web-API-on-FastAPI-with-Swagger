import services
import security
import models
import exceptions

from fastapi import Depends
from typing import AsyncGenerator, Annotated

from database import AsyncSession

_lock_service = services.Lock()


def get_token_service() -> services.Token:
    return security.token_service


async def get_data_service() -> AsyncGenerator[services.Data, None]:
    async with AsyncSession() as async_session:
        yield services.Data(async_session)


async def get_current_user(token: Annotated[str, Depends(security.oauth2_scheme)],
                           token_service: Annotated[services.Token, Depends(get_token_service)],
                           data_service: Annotated[services.Data, Depends(get_data_service)]) -> models.User:
    subject = token_service.get_subject(token)

    user = await data_service.get_user(subject['username'], subject['password'])

    if not user:
        raise exceptions.HTTPUnauthorizedException()

    return user


def get_lock_service() -> services.Lock:
    return _lock_service
