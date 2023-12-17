import schemas
import models
import dependencies

from fastapi import APIRouter, Depends, Form
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
                      data_service: Annotated[DataService, Depends(dependencies.get_data_service)],
                      is_show_deleted: bool = False):
    return await data_service.orders.get_few(current_user, is_show_deleted)


@router.put('', dependencies=[Depends(dependencies.RoleAccessChecker(Roles.CUSTOMER))])
async def update_order(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                       order_id: Annotated[int, Form()],
                       data_service: Annotated[DataService, Depends(dependencies.get_data_service)],
                       new_order_data: Annotated[schemas.OrderData, Depends(schemas.OrderData.as_form)]):
    if not await data_service.orders.get_user_order_existence_status(current_user, order_id):
        return schemas.Response(message='You do not have an order with this ID')

    await data_service.orders.change_data(order_id, new_order_data)

    return schemas.Response(message='Data updated')


@router.put('/status')
async def update_status(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                        order_id: Annotated[int, Form()],
                        status_id: Annotated[int, Form()],
                        data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    if not await data_service.orders.get_user_order_existence_status(current_user, order_id):
        return schemas.Response(message='You do not have an order with this ID')

    if not await data_service.statuses.get_existence_status(status_id):
        return schemas.Response(message='No such status exists')

    await data_service.orders.update_status(order_id, status_id)

    return schemas.Response(message='Status updated')


@router.put('/executor', dependencies=[Depends(dependencies.RoleAccessChecker(Roles.CUSTOMER))])
async def update_executor(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                          order_id: Annotated[int, Form()],
                          data_service: Annotated[DataService, Depends(dependencies.get_data_service)],
                          executor_id: Annotated[int, Form()]):
    if not await data_service.orders.get_user_order_existence_status(current_user, order_id):
        return schemas.Response(message='You do not have an order with this ID')

    if not await data_service.users.get_executor_existence_status(executor_id):
        return schemas.Response(message='No such executor exists')

    await data_service.orders.update_executor(order_id, executor_id)

    return schemas.Response(message='Executor updated')


@router.delete('', dependencies=[Depends(dependencies.RoleAccessChecker(Roles.CUSTOMER))])
async def delete_order(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                       order_id: Annotated[int, Form()],
                       data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    if not await data_service.orders.get_user_order_existence_status(current_user, order_id):
        return schemas.Response(message='You do not have an order with this ID')

    await data_service.orders.delete(order_id)

    return schemas.Response(message='Order deleted')
