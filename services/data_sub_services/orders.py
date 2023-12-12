import models

from typing import Sequence
from sqlalchemy import select

from services.data_sub_services.base import Base


class Orders(Base):
    async def get(self, user: models.User) -> Sequence[models.Order]:
        statement = select(models.Order).where(models.Order.customer_id == user.id)

        result = await self._async_session.execute(statement)

        return result.scalars().all()
