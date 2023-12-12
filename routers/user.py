import schemas
import models
import dependencies

from fastapi import APIRouter, Depends, Form
from typing import Annotated

from services.data import Data as DataService
from services.lock import Lock as LockService

router = APIRouter(prefix='/user', tags=['user'])


@router.get('', response_model=schemas.User)
async def read_user(current_user: Annotated[models.User, Depends(dependencies.get_current_user)]):
    return current_user


@router.put('/password', response_model=schemas.Response)
async def update_password(current_password: Annotated[str, Form()],
                          new_password: Annotated[str, Form()],
                          current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                          data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    if current_password == new_password:
        return schemas.Response(message='The current password and the new password are the same')

    if current_user.password != current_password:
        return schemas.Response(message='Current password is incorrect')

    await data_service.user.change_password(current_user, new_password)

    return schemas.Response(message='Password updated')


@router.put('/username', response_model=schemas.Response)
async def update_username(new_username: Annotated[str, Form()],
                          current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                          lock_service: Annotated[LockService, Depends(dependencies.get_lock_service)],
                          data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    if new_username == current_user.username:
        return schemas.Response(message='The new username and the current one are the same')

    async with await lock_service.get_lock(f'{models.User.__tablename__}_table'):
        if await data_service.user.get_existence_status(new_username):
            return schemas.Response(message='This username is already taken')

        await data_service.user.change_username(current_user, new_username)

    return schemas.Response(message='Username updated')
