class ChatsService:
    def __init__(self, repository):
        self._repository = repository

    async def create_chat(self, chat_dto):
        chat = await self._repository.create(chat_dto)
        return chat

    async def get_chat_by_id(self, chat_id):
        return await self._repository.get_by_id(chat_id)

    async def get_all_chats(self):
        return await self._repository.get_all()

    async def update_chat(self, chat_dto):
        return await self._repository.update(chat_dto)

    async def delete_chat(self, chat_id):
        return await self._repository.delete(chat_id)
