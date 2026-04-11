class UsersService:
    def __init__(self, repository):
        self._repository = repository

    async def create_user(self, user_data):
        return await self._repository.create(user_data)

    async def get_user_by_id(self, user_id):
        return await self._repository.get_by_id(user_id)

    async def get_all_users(self):
        return await self._repository.get_all()

    async def update_user(self, user_data):
        return await self._repository.update(user_data)

    async def delete_user(self, user_id):
        return await self._repository.delete(user_id)
