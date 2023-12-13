import models

from sqlalchemy import select

from services.data_subservices.base import Base


class Roles(Base):
    async def get_one(self, key: str) -> models.Role:
        statement = select(models.Role).where(models.Role.key == key)

        result = await self._async_session.execute(statement)

        return result.scalar()
