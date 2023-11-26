import models

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from sqlalchemy import select


async def get_users(database_session: AsyncSession) -> Sequence[models.User]:
    statement = select(models.User)

    result = await database_session.execute(statement)

    return result.scalars().all()
