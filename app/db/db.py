from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
import ssl

from app.config import DB

ssl_context = ssl.create_default_context()

engine = create_async_engine(
    DB,
    connect_args={
        "ssl": ssl_context,
    },
    pool_pre_ping=True,
    pool_recycle=1800,
)

sessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionLocal() as ass:
        yield ass
