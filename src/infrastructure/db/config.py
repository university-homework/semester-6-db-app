from sqlalchemy.ext.asyncio import create_async_engine  # noqa

from infrastructure.env.config import env

DB_USER = env.str('DB_USER', 'postgres')
DB_PASSWORD = env.str('DB_PASSWORD', '')
DB_HOST = env.str('DB_HOST', 'postgres')
DB_PORT = env.int('DB_PORT', 5432)
DB_NAME = env.str('DB_NAME', 'postgres')

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DB_URL)
