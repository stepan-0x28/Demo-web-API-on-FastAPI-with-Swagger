from sqlalchemy.ext.asyncio import AsyncSession


class Base:
    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session
