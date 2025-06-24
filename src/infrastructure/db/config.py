from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # noqa
from sqlmodel.ext.asyncio.session import AsyncSession

from infrastructure.env.config import env

DB_USER = env.str('DB_USER', 'postgres')
DB_PASSWORD = env.str('DB_PASSWORD', '')
DB_HOST = env.str('DB_HOST', 'postgres')
DB_PORT = env.int('DB_PORT', 5432)
DB_NAME = env.str('DB_NAME', 'postgres')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DB_URL)
AsyncSessionLocal = async_sessionmaker(engine, autocommit=False, class_=AsyncSession)


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
