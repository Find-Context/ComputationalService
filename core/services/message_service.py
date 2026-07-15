from core.dto import MessageDTO

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from numpy import argmax

from domain.models.mongo import ContextMessageDao

_model = SentenceTransformer("all-MiniLM-L6-v2")


class MessageService:
    def __init__(self, repository):
        self._repository = repository

    async def create_message(self, message_dto):
        await self._repository.create(message_dto)

    async def get_message_by_id(self, message_id):
        return await self._repository.get_by_id(message_id)

    async def delete_message(self, message_id):
        return await self._repository.delete(message_id)

    async def fast_search(self, message_dto: MessageDTO):
        context_message = ContextMessageDao(
            chat_id=message_dto.chat_id,
            embedding=_model.encode([message_dto.text]).tolist()[0],
        )
        return await self._repository.fast_search(context_message)
