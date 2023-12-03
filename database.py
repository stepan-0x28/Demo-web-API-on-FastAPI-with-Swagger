from os import environ
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

username = environ.get('DATABASE_USERNAME')
password = environ.get('DATABASE_PASSWORD')
host = environ.get('DATABASE_HOST')
name = environ.get('DATABASE_NAME')

async_engine = create_async_engine(f'postgresql+asyncpg://{username}:{password}@{host}/{name}')

AsyncSession = async_sessionmaker(async_engine)
