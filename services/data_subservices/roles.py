import models

from typing import Sequence
from sqlalchemy import select, func

from services.data_subservices.base import Base


class Roles(Base):
    async def get_few(self) -> Sequence[models.Role]:
        statement = select(models.Role)

        return await self._execute_and_get_all(statement)

    async def get_existence_status(self, id_: int) -> bool:
        statement = select(func.count()).where(models.Role.id == id_)

        return bool(await self._execute_and_get_one(statement))
