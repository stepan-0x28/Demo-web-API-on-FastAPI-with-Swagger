import uvicorn

import schemas
import services
import dependencies
import exceptions
import models

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, List

app = FastAPI()


@app.post('/token', response_model=schemas.Token)
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                       data_service: Annotated[services.Data, Depends(dependencies.get_data_service)],
                       token_service: Annotated[services.Token, Depends(dependencies.get_token_service)]):
    user = await data_service.get_user(form_data.username, form_data.password)

    if not user:
        raise exceptions.HTTPUnauthorizedException()

    token = token_service.create({'username': user.username, 'password': user.password})

    return schemas.Token(access_token=token, token_type='bearer')


@app.get('/user', response_model=schemas.User)
async def read_user(current_user: Annotated[models.User, Depends(dependencies.get_current_user)]):
    return current_user


@app.put('/password', response_model=schemas.Response)
async def update_password(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                          password_update_data: schemas.PasswordUpdateData,
                          data_service: Annotated[services.Data, Depends(dependencies.get_data_service)]):
    if current_user.password != password_update_data.current_password:
        raise exceptions.HTTPForbiddenException()

    await data_service.change_password(current_user, password_update_data.new_password)

    return schemas.Response(message='Password updated')


@app.get('/orders', response_model=List[schemas.Order])
async def read_orders(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                      data_service: Annotated[services.Data, Depends(dependencies.get_data_service)]):
    return await data_service.get_user_orders(current_user)


if __name__ == '__main__':
    uvicorn.run(app)
