import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

db = declarative_base()
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env")
)  # noqa


db_engine = create_async_engine(
    f"postgresql+asyncpg://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('HOST_DB')}:5432/{os.environ.get('DB_NAME')}",  # noqa
    echo=True,
    future=True,
)


async def get_session() -> AsyncSession:
    async with AsyncSession(db_engine, expire_on_commit=False) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
