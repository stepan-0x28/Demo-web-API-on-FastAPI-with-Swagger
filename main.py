import uvicorn

import schemas
import services

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from database import get_database_session

app = FastAPI()


@app.get('/', response_model=schemas.HelloWorld)
async def root():
    return schemas.HelloWorld()


@app.get('/users', response_model=List[schemas.User])
async def users(database_session: Annotated[AsyncSession, Depends(get_database_session)]):
    return await services.get_users(database_session)


if __name__ == '__main__':
    uvicorn.run(app)
