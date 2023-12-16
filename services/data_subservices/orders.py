import models
import schemas

from sqlalchemy import select, insert, func, update, false
from typing import Sequence

from services.data_subservices.base import Base
from enumerations import Statuses, Roles


class Orders(Base):
    async def create(self, user: models.User, new_order_details: schemas.OrderIn):
        status_id_subquery = select(models.Status.id).where(
            models.Status.key == Statuses.NEW
        ).scalar_subquery()

        statement = insert(models.Order).values(customer_id=user.id,
                                                **new_order_details.model_dump(),
                                                status_id=status_id_subquery)

        await self._execute(statement)

        await self._commit()

    async def get_few(self, user: models.User) -> Sequence[models.Order]:
        column = models.Order.customer_id

        if user.role.key == Roles.EXECUTOR:
            column = models.Order.executor_id

        statement = select(models.Order).where(
            column == user.id).where(
            models.Order.is_deleted == false()
        )

        return await self._execute_and_get_all(statement)

    async def get_user_order_existence_status(self, user: models.User, order_id: int) -> bool:
        column = models.Order.customer_id

        if user.role.key == Roles.EXECUTOR:
            column = models.Order.executor_id

        statement = select(func.count()).where(
            models.Order.id == order_id).where(
            column == user.id).where(
            models.Order.is_deleted == false()
        )

        return bool(await self._execute_and_get_one(statement))

    async def update_status(self, order_id: int, status_id: int):
        statement = update(models.Order).where(models.Order.id == order_id).values(status_id=status_id)

        await self._execute(statement)

        await self._commit()

    async def delete(self, order_id: int):
        statement = update(models.Order).where(models.Order.id == order_id).values(is_deleted=True)

        await self._execute(statement)

        await self._commit()
