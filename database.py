from os import environ
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

username = environ.get('DATABASE_USERNAME')
password = environ.get('DATABASE_PASSWORD')
host = environ.get('DATABASE_HOST')
name = environ.get('DATABASE_NAME')

AsyncAppSession = async_sessionmaker(create_async_engine(f'postgresql+asyncpg://{username}:{password}@{host}/{name}'))


async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncAppSession() as async_session:
        yield async_session
