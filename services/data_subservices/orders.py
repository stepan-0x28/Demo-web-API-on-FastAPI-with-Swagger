import models

from typing import Sequence
from sqlalchemy import select

from services.data_subservices.base import Base
from enumerations import Roles


class Orders(Base):
    async def get_few(self, user: models.User) -> Sequence[models.Order]:
        column = models.Order.customer_id

        if user.role.key == Roles.EXECUTOR:
            column = models.Order.executor_id

        statement = select(models.Order).where(column == user.id)

        result = await self._async_session.execute(statement)

        return result.scalars().all()
