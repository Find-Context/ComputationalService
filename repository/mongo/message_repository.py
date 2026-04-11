from pymongo.errors import DuplicateKeyError

from repository.context.mongo_context import mongo
from models import Message, MessageDTO

from repository.abstractions import AbstractRepository

from mapper import map_message_dto_to_dao


class MessageRepository(AbstractRepository):
    def __init__(self, context):
        self._context = context

    async def create(self, entity: MessageDTO):
        try:
            await mongo.get_database.get_collection("messages").insert_one(
                map_message_dto_to_dao(entity).model_dump(mode='json')
            )
        except DuplicateKeyError as e:
            print(f"Duplicate key error: {e}")
            raise e
        except Exception as e:
            print(f"Error inserting message: {e}")
            return

    async def get_by_id(self, id: int):
        try:
            return await self._context.get_database.get_collection("messages").find_one({"id": id})
        except Exception as e:
            print(f"Error getting message: {e}")
            raise e

    async def get_all(self):
        pass

    async def update(self, entity: Message):  # TODO: implement update method
        pass

    async def delete(self, id: int):
        try:
            result = await mongo.get_database.get_collection("messages").delete_one({"id": id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting message: {e}")
            raise e
