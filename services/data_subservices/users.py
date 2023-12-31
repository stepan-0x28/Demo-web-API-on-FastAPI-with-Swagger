import models
import schemas

from typing import Optional, Sequence
from sqlalchemy import insert, select, update, func
from sqlalchemy.orm import joinedload

from services.data_subservices.base import Base
from enumerations import Roles


class Users(Base):
    async def create(self, new_user_details: schemas.UserIn):
        statement = insert(models.User).values(new_user_details.model_dump())

        await self._execute(statement)

        await self._commit()

    async def get_one(self, username: str, password: str) -> Optional[models.User]:
        statement = select(models.User).where(
            models.User.username == username).where(
            models.User.password == password
        ).options(joinedload(models.User.role))

        return await self._execute_and_get_one(statement)

    async def change_data(self, user: models.User, new_user_data: schemas.UserData):
        statement = update(models.User).where(models.User.id == user.id).values(new_user_data.model_dump())

        await self._execute(statement)

        await self._commit()

    async def change_password(self, user: models.User, new_password: str):
        statement = update(models.User).where(models.User.id == user.id).values({models.User.password: new_password})

        await self._execute(statement)

        await self._commit()

    async def get_existence_status(self, username: str) -> bool:
        return await self._get_existence_status(models.User.username == username)

    async def get_executor_existence_status(self, id_: int) -> bool:
        statement = select(func.count()).select_from(models.User).join(models.Role).where(
            models.User.id == id_).where(
            models.Role.key == Roles.EXECUTOR
        )

        return bool(await self._execute_and_get_one(statement))

    async def change_username(self, user: models.User, new_username: str):
        statement = update(models.User).where(models.User.id == user.id).values({models.User.username: new_username})

        await self._execute(statement)

        await self._commit()

    async def get_executors(self) -> Sequence[models.User]:
        statement = select(models.User).join(models.Role).where(models.Role.key == Roles.EXECUTOR)

        return await self._execute_and_get_all(statement)
