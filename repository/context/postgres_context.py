from core import settings
from core.exceptions.database_connection_error import DatabaseConnectionError
from . import Singleton

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Postgres(metaclass=Singleton):

    def __init__(self):
        try:
            self._engine = create_async_engine(
                f"postgresql+asyncpg://"
                f"{settings.postgres_user}:{settings.postgres_password}"
                f"@{settings.postgres_host}:{settings.postgres_port}"
                f"/{settings.postgres_db}",
                pool_size=20
            )
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise DatabaseConnectionError(f"Error connecting to PostgreSQL: {e}")

        self._sessionmaker = async_sessionmaker(self._engine)

    def get_session(self):
        return self._sessionmaker()


_postgres_context = Postgres()
