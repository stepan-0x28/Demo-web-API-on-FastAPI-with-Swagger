import models

from typing import Sequence
from sqlalchemy import select, func

from services.data_subservices.base import Base


class Roles(Base):
    async def get_few(self) -> Sequence[models.Role]:
        statement = select(models.Role)

        result = await self._async_session.execute(statement)

        return result.scalars().all()

    async def get_existence_status(self, id_: int) -> bool:
        statement = select(func.count()).where(models.Role.id == id_)

        result = await self._async_session.execute(statement)

        return bool(result.scalar())
