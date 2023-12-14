import schemas
import dependencies

from fastapi import APIRouter, Depends
from typing import List, Annotated

from services.data import Data as DataService

router = APIRouter(prefix='/statuses', tags=['statuses'])


@router.get('', response_model=List[schemas.Status])
async def read_statuses(data_service: Annotated[DataService, Depends(dependencies.get_data_service)]):
    return await data_service.statuses.get_few()
