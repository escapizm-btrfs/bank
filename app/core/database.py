from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import Settings

settings_db = Settings()

#DATABASE_URL = "postgresql+asyncpg://escapizm:32151812@127.0.0.1:5432/main_db"

DATABASE_URL = f"postgresql+asyncpg://{settings_db.DB_USER}:{settings_db.DB_PASSWORD}@{settings_db.DB_HOST}:{settings_db.DB_PORT}/{settings_db.DB_NAME}"

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

