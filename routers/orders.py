import schemas
import models
import dependencies

from fastapi import APIRouter, Depends
from typing import List, Annotated

from services.data import Data as DataService

router = APIRouter(prefix='/orders', tags=['orders'])


@router.get('', response_model=List[schemas.Order])
async def read_orders(current_user: Annotated[models.User, Depends(dependencies.get_current_user)],
                      data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    return await data_service.orders.get(current_user)
