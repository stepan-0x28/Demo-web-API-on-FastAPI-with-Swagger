import schemas
import models
import dependencies

from fastapi import APIRouter, Depends
from typing import List, Annotated

from enumerations import Roles
from services.data import Data as DataService

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('', dependencies=[Depends(dependencies.RoleAccessChecker(Roles.CUSTOMER))])
async def create_order(new_order_details: Annotated[schemas.OrderIn, Depends(schemas.OrderIn.as_form)],
                       data_service: Annotated[DataService, Depends(dependencies.get_data_service)],
                       current_user: Annotated[models.User, Depends(dependencies.get_current_user)]):
    if not await data_service.users.get_executor_existence_status(new_order_details.executor_id):
        return schemas.Response(message='No such executor exists')

    await data_service.orders.create(current_user, new_order_details)

    return schemas.Response(message='Order created')


@router.get('', response_model=List[schemas.OrderOut])
async def read_orders(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                      data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    return await data_service.orders.get_few(current_user)
