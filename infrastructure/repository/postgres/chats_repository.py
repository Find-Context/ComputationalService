from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError

from core.exceptions import DuplicatedPrimaryKeyError, NoContentError
from domain.models import Chats
from core.dto import ChatsDTO

from infrastructure.repository.abstractions import AbstractRepository

from core.mapper import map_chats_dto_to_dao


class ChatsRepository(AbstractRepository):
    def __init__(self, session):
        self._session = session

    async def create(self, entity: ChatsDTO):
        try:
            mapped_entity = map_chats_dto_to_dao(entity)
            self._session.add(mapped_entity)
            await self._session.flush()

            return mapped_entity
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
            chat = await self._session.get(Chats, id)
            if chat:
                return chat
            raise NoContentError(f"No chat found with id: {id}")
        except Exception as e:
            print(f"Error retrieving chat: {e}")
            raise e

    async def get_all(self):
        try:
            result = await self._session.execute(select(Chats))
            return result.scalars().all()
        except Exception as e:
            print(f"Error retrieving chats: {e}")
            raise e

    async def update(self, entity: ChatsDTO):
        try:
            return await self._session.merge(map_chats_dto_to_dao(entity))
        except DataError as e:
            print(f"Data error while updating chat: {e}")
            raise e
        except Exception as e:
            print(f"Error updating chat: {e}")
            raise e

    async def delete(self, id: int):
        try:
            chat = await self._session.get(Chats, id)
            if chat:
                await self._session.delete(chat)
                return True
            raise NoContentError(f"No chat found with id: {id}")
        except NoContentError:
            raise
        except Exception as e:
            print(f"Error deleting chat: {e}")
            raise e
