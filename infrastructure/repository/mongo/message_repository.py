from pymongo.errors import DuplicateKeyError

from core.exceptions import DuplicatedPrimaryKeyError
from domain.models.mongo import ContextMessageDao
from domain.models import Message, MessageDTO

from infrastructure.repository.abstractions import AbstractRepository

from mapper import map_message_dto_to_dao

from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")


class MessageRepository(AbstractRepository):
    def __init__(self, context):
        self._context = context

    async def create(self, entity: MessageDTO):
        try:
            await self._context.get_database.get_collection("messages").insert_one(
                map_message_dto_to_dao(entity, _model.encode([entity.text]).tolist()[0]).model_dump(mode='json')
            )
        except DuplicateKeyError as e:
            print(f"Duplicate key error: {e}")
            raise DuplicatedPrimaryKeyError(str(e))
        except Exception as e:
            print(f"Error inserting message: {e}")
            raise e

    async def get_by_id(self, id: int):
        try:
            return await self._context.get_database.get_collection("messages").find_one({"id": id})
        except Exception as e:
            print(f"Error getting message: {e}")
            raise e

    async def fast_search(self, context_message: ContextMessageDao):
        try:
            pipeline = [
                {
                    "$match": {
                        "chat_id": context_message.chat_id
                    }
                },
                {
                    "$addFields": {
                        "similarity": {
                            "$reduce": {
                                "input": {"$range": [0, len(context_message.embedding)]},
                                "initialValue": 0,
                                "in": {
                                    "$add": [
                                        "$$value",
                                        {
                                            "$multiply": [
                                                {"$arrayElemAt": ["$vector", "$$this"]},
                                                {"$arrayElemAt": [context_message.embedding, "$$this"]}
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    }
                },
                {
                    "$sort": {"similarity": -1}
                },
                {
                    "$limit": 1
                },
                {
                    "$project": {
                        "_id": 0,
                        "message_id": 1,
                    }
                }
            ]

            aggregated = await self._context.get_database.get_collection("messages").aggregate(pipeline)
            result = await aggregated.to_list(length=1)
            if not result:
                return None
            return result[0].get("message_id")

        except Exception as e:
            print(f"Error performing fast search: {e}")
            raise e

    async def get_all(self):
        pass

    async def update(self, entity: Message):  # TODO: implement update method
        pass

    async def delete(self, id: int):
        try:
            result = await self._context.get_database.get_collection("messages").delete_one({"_id": id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting message: {e}")
            raise e
