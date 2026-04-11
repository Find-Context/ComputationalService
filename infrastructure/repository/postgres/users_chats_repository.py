from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError

from core.exceptions.entity_error import DuplicatedPrimaryKeyError
from domain.models import UsersChats

from infrastructure.repository.abstractions import AbstractRepository


class UsersChatsRepository(AbstractRepository):
    def __init__(self, context):
        self._context = context

    async def create(self, user_id: int, chat_id: int):
        try:
            users_chats = UsersChats(user_id=user_id, chat_id=chat_id)
            self._context.get_session.add(users_chats)
            await self._context.get_session.flush()

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

    async def get_by_id(self, id: int):
        pass

    async def get_all(self):
        try:
            result = await self._context.get_session.execute(select(UsersChats))
            return result.all()
        except Exception as e:
            print(f"Error retrieving user - chat connection: {e}")
            raise e

    async def update(self, entity):
        pass

    async def delete(self, user_id: int, chat_id: int):
        try:
            users_chats = UsersChats(user_id=user_id, chat_id=chat_id)
            entity = await self._context.get_session.get(users_chats)
            if entity:
                await self._context.get_session.delete(entity)
                return True
            raise DataError
        except Exception as e:
            print(f"Error deleting user - chat connection: {e}")
            raise e
