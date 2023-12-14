import schemas
import dependencies

from fastapi import APIRouter, Depends
from typing import List, Annotated

from services.data import Data as DataService

router = APIRouter(prefix='/roles', tags=['roles'])


@router.get('', response_model=List[schemas.Role])
async def read_roles(data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    return await data_service.roles.get_few()
