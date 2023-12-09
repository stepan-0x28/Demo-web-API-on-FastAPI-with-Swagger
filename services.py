import json

import models

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence, Dict
from sqlalchemy import select, update
from jose import jwt


class Data:
    def __init__(self, async_session: AsyncSession):
        self.__async_session = async_session

    async def get_user(self, username: str, password: str) -> Optional[models.User]:
        statement = select(models.User).join(models.Role).where(
            models.User.username == username).where(
            models.User.password == password).where(
            models.Role.key == 'customer'
        )

        result = await self.__async_session.execute(statement)

        return result.scalar()

    async def get_user_orders(self, user: models.User) -> Sequence[models.Order]:
        statement = select(models.Order).where(models.Order.customer_id == user.id)

        result = await self.__async_session.execute(statement)

        return result.scalars().all()

    async def change_password(self, user: models.User, new_password: str):
        statement = update(models.User).where(models.User.id == user.id).values({models.User.password: new_password})

        await self.__async_session.execute(statement)

        await self.__async_session.commit()


class Token:
    def __init__(self, key: str):
        self.__secret_key = key

    def create(self, subject: Dict) -> str:
        claims = {'sub': json.dumps(subject)}

        return jwt.encode(claims, self.__secret_key)

    def get_subject(self, token: str) -> Dict:
        claims = jwt.decode(token, self.__secret_key)

        return json.loads(claims['sub'])
