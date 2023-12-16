import models

from typing import Sequence
from sqlalchemy import select

from services.data_subservices.base import Base


class Statuses(Base):
    async def get_few(self) -> Sequence[models.Role]:
        statement = select(models.Status)

        return await self._execute_and_get_all(statement)

    async def get_existence_status(self, id_: int) -> bool:
        return await self._get_existence_status(models.Status.id == id_)
