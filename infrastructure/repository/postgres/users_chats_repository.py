from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError

from core.exceptions.entity_error import DuplicatedPrimaryKeyError
from core.exceptions import NoContentError
from domain.models import UsersChats

from infrastructure.repository.abstractions import AbstractRepository


class UsersChatsRepository(AbstractRepository):
    def __init__(self, session):
        self._session = session

    async def create(self, user_id: int, chat_id: int):
        try:
            users_chats = UsersChats(user_id=user_id, chat_id=chat_id)
            self._session.add(users_chats)
            await self._session.flush()

            return users_chats
        except IntegrityError as e:
            print(f"Duplicated primary keys while creating new user - chat connection: {e}")
            raise DuplicatedPrimaryKeyError(str(e))
        except DataError as e:
            print(f"Data error while creating new user - chat connection: {e}")
            raise e
        except Exception as e:
            print(f"Error creating user - chat connection: {e}")
            raise e

    async def get_by_id(self, user_id: int, chat_id: int):
        try:
            entity = await self._session.get(UsersChats, (user_id, chat_id))
            if entity:
                return entity
            raise NoContentError(
                f"No user - chat connection found for user_id: {user_id}, chat_id: {chat_id}"
            )
        except NoContentError:
            raise
        except Exception as e:
            print(f"Error retrieving user - chat connection: {e}")
            raise e

    async def get_all(self):
        try:
            result = await self._session.execute(select(UsersChats))
            return result.scalars().all()
        except Exception as e:
            print(f"Error retrieving user - chat connection: {e}")
            raise e

    async def get_all_by_user_id(self, user_id: int):
        try:
            result = await self._session.execute(
                select(UsersChats).where(UsersChats.user_id == user_id)
            )
            return result.scalars().all()
        except Exception as e:
            print(f"Error retrieving user - chat connections for user: {e}")
            raise e

    async def update(self, entity):
        # UsersChats is a pure association table (composite primary key only,
        # no other columns), so there is nothing to mutate in place. Callers
        # that need to re-point a connection should delete the old pair and
        # create a new one instead.
        raise NotImplementedError("UsersChats has no mutable fields; use delete + create instead.")

    async def delete(self, user_id: int, chat_id: int):
        try:
            entity = await self._session.get(UsersChats, (user_id, chat_id))
            if entity:
                await self._session.delete(entity)
                return True
            raise NoContentError(
                f"No user - chat connection found for user_id: {user_id}, chat_id: {chat_id}"
            )
        except NoContentError:
            raise
        except Exception as e:
            print(f"Error deleting user - chat connection: {e}")
            raise e
