import uvicorn

import schemas
import services
import dependencies
import exceptions
import models

from fastapi import FastAPI, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, List

app = FastAPI()


@app.post('/token', response_model=schemas.Token, tags=['token'])
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       data_service: Annotated[services.Data, Depends(dependencies.get_data_service)],
                       token_service: Annotated[services.Token, Depends(dependencies.get_token_service)]):
    user = await data_service.get_user(form_data.username, form_data.password)

    if not user:
        raise exceptions.HTTPUnauthorizedException()

    token = token_service.create({'username': user.username, 'password': user.password})

    return schemas.Token(access_token=token, token_type='bearer')


@app.get('/user', response_model=schemas.User, tags=['user'])
async def read_user(current_user: Annotated[models.User, Depends(dependencies.get_current_user)]):
    return current_user


@app.put('/user/password', response_model=schemas.Response, tags=['user'])
async def update_password(current_password: Annotated[str, Form()],
                          new_password: Annotated[str, Form()],
                          current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                          data_service: Annotated[services.Data, Depends(dependencies.get_data_service)]):
    if current_password == new_password:
        return schemas.Response(message='The current password and the new password are the same')

    if current_user.password != current_password:
        return schemas.Response(message='Current password is incorrect')

    await data_service.change_password(current_user, new_password)

    return schemas.Response(message='Password updated')


@app.put('/user/username', response_model=schemas.Response, tags=['user'])
async def update_username(new_username: Annotated[str, Form()],
                          current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                          lock_service: Annotated[services.Lock, Depends(dependencies.get_lock_service)],
                          data_service: Annotated[services.Data, Depends(dependencies.get_data_service)]):
    if new_username == current_user.username:
        return schemas.Response(message='The new username and the current one are the same')

    async with await lock_service.get_lock(f'{models.User.__tablename__}_table'):
        if await data_service.get_user_existence_status(new_username):
            return schemas.Response(message='This username is already taken')

        await data_service.change_username(current_user, new_username)

    return schemas.Response(message='Username updated')


@app.get('/orders', response_model=List[schemas.Order], tags=['orders'])
async def read_orders(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                      data_service: Annotated[services.Data, Depends(dependencies.get_data_service)]):
    return await data_service.get_user_orders(current_user)


if __name__ == '__main__':
    uvicorn.run(app)
