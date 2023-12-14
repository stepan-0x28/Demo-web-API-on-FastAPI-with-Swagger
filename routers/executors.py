import schemas
import dependencies

from fastapi import APIRouter, Depends
from typing import List, Annotated

from services.data import Data as DataService

router = APIRouter(prefix='/executors', tags=['executors'])


@router.get('', response_model=List[schemas.UserOut])
async def read_executors(data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    return await data_service.users.get_executors()
