class MessageService:
    def __init__(self, repository):
        self._repository = repository

    async def create_message(self, message_dto):
        await self._repository.create(message_dto)

    async def get_message_by_id(self, message_id):
        return await self._repository.get_by_id(message_id)

    async def delete_message(self, message_id):
        return await self._repository.delete(message_id)
