from infrastructure.db.config import DB_URL


def get_db_url() -> str:
    url = DB_URL
    if DB_URL.startswith('postgresql+asyncpg://'):
        url = DB_URL.replace('postgresql+asyncpg://', 'postgresql+psycopg2://', 1)
    return url
