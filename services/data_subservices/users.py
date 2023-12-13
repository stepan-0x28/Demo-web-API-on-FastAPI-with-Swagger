import models

from typing import Optional
from sqlalchemy import select, update, func

from services.data_subservices.base import Base


class Users(Base):
    async def create(self, new_user: models.User):
        self._async_session.add(new_user)

        await self._async_session.commit()

    async def get_one(self, username: str, password: str) -> Optional[models.User]:
        statement = select(models.User).join(models.Role).where(
            models.User.username == username).where(
            models.User.password == password).where(
            models.Role.key == 'customer'
        )

        result = await self._async_session.execute(statement)

        return result.scalar()

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
