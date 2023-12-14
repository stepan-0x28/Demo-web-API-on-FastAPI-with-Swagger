import models

from typing import Sequence
from sqlalchemy import select

from services.data_subservices.base import Base


class Statuses(Base):
    async def get_few(self) -> Sequence[models.Role]:
        statement = select(models.Status)

        result = await self._async_session.execute(statement)

        return result.scalars().all()
