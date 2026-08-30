from pymongo.errors import DuplicateKeyError

from core.exceptions import DuplicatedPrimaryKeyError, NoContentError
from domain.models.mongo import ContextMessageDao
from core.dto import MessageDTO

from infrastructure.repository.abstractions import AbstractRepository

from core.mapper import map_message_dto_to_dao

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

    async def get_by_id(self, message_id: int):
        try:
            message = await self._context.get_database.get_collection("messages").find_one(
                {"message_id": message_id}
            )
            if message:
                return message
            raise NoContentError(f"No message found with message_id: {message_id}")
        except NoContentError:
            raise
        except Exception as e:
            print(f"Error getting message: {e}")
            raise e

    async def get_all_by_chat_id(self, chat_id: int):
        try:
            cursor = self._context.get_database.get_collection("messages").find(
                {"chat_id": chat_id}
            ).sort("created_at", -1)
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error getting messages by chat id: {e}")
            raise e

    async def fast_search(self, context_message: ContextMessageDao):
        try:
            pipeline = [
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
            print(result[0].get("chat_id") +" " + result[0].get("text"))
            return result[0].get("message_id")

        except Exception as e:
            print(f"Error performing fast search: {e}")
            raise e

    async def get_all(self):
        try:
            cursor = self._context.get_database.get_collection("messages").find({})
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error getting all messages: {e}")
            raise e

    async def update(self, entity: MessageDTO):
        try:
            embedding = _model.encode([entity.text]).tolist()[0]
            message_dao = map_message_dto_to_dao(entity, embedding)

            result = await self._context.get_database.get_collection("messages").update_one(
                {"chat_id": entity.chat_id, "message_id": entity.message_id},
                {"$set": message_dao.model_dump(mode='json')},
            )
            if result.matched_count == 0:
                raise NoContentError(
                    f"No message found with chat_id: {entity.chat_id}, message_id: {entity.message_id}"
                )
            return result.modified_count > 0
        except NoContentError:
            raise
        except Exception as e:
            print(f"Error updating message: {e}")
            raise e

    async def delete(self, message_id: int):
        try:
            result = await self._context.get_database.get_collection("messages").delete_one(
                {"message_id": message_id}
            )
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting message: {e}")
            raise e
