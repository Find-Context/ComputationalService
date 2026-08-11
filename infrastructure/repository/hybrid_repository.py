from core.exceptions import NoContentError
from domain.models import Chats

__all__ = ["HybridRepository"]


class HybridRepository:
    """
    Combines the relational store (PostgreSQL: chats/users metadata) with the
    document store (MongoDB: message content and embeddings) to build a
    unified view of a chat, e.g. chat metadata together with its message
    history.
    """

    def __init__(self, session, mongo_context):
        self._session = session
        self._mongo_context = mongo_context

    async def get_all_messages_by_chat_id(self, chat_id: int):
        try:
            cursor = self._mongo_context.get_database.get_collection("messages").find(
                {"chat_id": chat_id}
            ).sort("created_at", -1)
            return await cursor.to_list(length=None)
        except Exception as e:
            print(f"Error getting messages by chat id: {e}")
            raise e

    async def get_chat_with_messages(self, chat_id: int):
        try:
            chat = await self._session.get(Chats, chat_id)
            if chat is None:
                raise NoContentError(f"No chat found with id: {chat_id}")

            messages = await self.get_all_messages_by_chat_id(chat_id)

            return {
                "chat": chat,
                "messages": messages,
            }
        except NoContentError:
            raise
        except Exception as e:
            print(f"Error getting chat with messages: {e}")
            raise e
