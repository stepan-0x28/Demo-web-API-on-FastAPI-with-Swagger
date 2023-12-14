from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, Update, Result
from typing import Union, Any, Sequence


class Base:
    def __init__(self, async_session: AsyncSession):
        self.__async_session = async_session

    async def _execute(self, statement: Union[Select, Update]) -> Result[Any]:
        return await self.__async_session.execute(statement)

    async def _execute_and_get_all(self, statement: Union[Select, Update]) -> Sequence[Any]:
        result = await self._execute(statement)

        return result.scalars().all()

    async def _execute_and_get_one(self, statement: Union[Select, Update]) -> Any:
        result = await self._execute(statement)

        return result.scalar()

    def _add(self, instance: object):
        self.__async_session.add(instance)

    async def _commit(self):
        await self.__async_session.commit()
