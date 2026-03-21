from core import settings
from . import Singleton

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Postgres(metaclass=Singleton):

    def __init__(self):
        self._engine = create_async_engine(
            f"postgresql+asyncpg://"
            f"{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}:{settings.postgres_port}"
            f"/{settings.postgres_db}",
            pool_size=20
        )

        self._sessionmaker = async_sessionmaker(self._engine)

    def get_session(self):
        return self._sessionmaker()


postgres = Postgres()
