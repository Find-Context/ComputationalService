from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError

from core.exceptions import DuplicatedPrimaryKeyError
from models import Chats, ChatsDTO

from repository.abstractions import AbstractRepository

from mapper import map_chats_dto_to_dao


class ChatsRepository(AbstractRepository):
    def __init__(self, context):
        self._context = context

    async def create(self, entity: ChatsDTO):
        try:
            mapped_entity = map_chats_dto_to_dao(entity)
            await self._context.get_session.add(mapped_entity)
            await self._context.get_session.flush()

            return entity
        except IntegrityError as e:
            print(f"Duplicated primary keys while creating new chat: {e}")
            raise DuplicatedPrimaryKeyError(str(e))
        except DataError as e:
            print(f"Data error while creating new chat: {e}")
            raise e
        except Exception as e:
            print(f"Error creating chat: {e}")
            raise e

    async def get_by_id(self, id: int):
        try:
            return await self._context.get_session.get(Chats, id)
        except Exception as e:
            print(f"Error retrieving chat: {e}")
            raise e

    async def get_all(self):
        try:
            result = await self._context.get_session.execute(select(Chats))
            return result.all()
        except Exception as e:
            print(f"Error retrieving chats: {e}")
            raise e

    async def update(self, entity: ChatsDTO):
        try:
            return await self._context.get_session.merge(map_chats_dto_to_dao(entity))
        except DataError as e:
            print(f"Data error while updating chat: {e}")
            raise e
        except Exception as e:
            print(f"Error updating chat: {e}")
            raise e

    async def delete(self, id: int):
        try:
            chat = await self._context.get_session.get(Chats, id)
            if chat:
                await self._context.get_session.delete(chat)
                return True
            raise DataError
        except Exception as e:
            print(f"Error deleting chat: {e}")
            raise e
