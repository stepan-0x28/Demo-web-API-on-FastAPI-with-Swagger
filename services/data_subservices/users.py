import models
import schemas

from typing import Optional, Sequence
from sqlalchemy import select, update, func
from sqlalchemy.orm import joinedload

from services.data_subservices.base import Base
from enumerations import Roles


class Users(Base):
    async def create(self, new_user: models.User):
        self._async_session.add(new_user)

        await self._async_session.commit()

    async def get_one(self, username: str, password: str) -> Optional[models.User]:
        statement = select(models.User).where(
            models.User.username == username).where(
            models.User.password == password
        ).options(joinedload(models.User.role))

        result = await self._async_session.execute(statement)

        return result.scalar()

    async def change_data(self, user_id: int, new_user_data: schemas.UserData):
        statement = update(models.User).where(models.User.id == user_id).values(new_user_data)

        await self._async_session.execute(statement)

        await self._async_session.commit()

    async def change_password(self, user: models.User, new_password: str):
        statement = update(models.User).where(models.User.id == user.id).values({models.User.password: new_password})

        await self._async_session.execute(statement)

        await self._async_session.commit()

    async def get_existence_status(self, username: str) -> bool:
        statement = select(func.count()).where(models.User.username == username)

        result = await self._async_session.execute(statement)

        return bool(result.scalar())

    async def change_username(self, user: models.User, new_username: str):
        statement = update(models.User).where(models.User.id == user.id).values({models.User.username: new_username})

        await self._async_session.execute(statement)

        await self._async_session.commit()

    async def get_executors(self) -> Sequence[models.User]:
        statement = select(models.User).join(models.Role).where(models.Role.key == Roles.EXECUTOR)

        result = await self._async_session.execute(statement)

        return result.scalars().all()
