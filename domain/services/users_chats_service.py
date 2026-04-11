class UsersChatsService:
    def __init__(self, repository):
        self._repository = repository

    async def create_user_chat(self, user_id: int, chat_id: int):
        return await self._repository.create_user_chat(user_id, chat_id)

    async def get_all_user_chats(self):
        return await self._repository.get_all_user_chats()

    async def delete_user_chat(self, user_id: int, chat_id: int):
        return await self._repository.delete_user_chat(user_id, chat_id)

