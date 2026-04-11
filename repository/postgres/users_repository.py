from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError

from core.exceptions.entity_error import DuplicatedPrimaryKeyError
from models import Users, UsersDTO

from repository.abstractions import AbstractRepository

from mapper import map_users_dto_to_dao


class UsersRepository(AbstractRepository):
    def __init__(self, context):
        self._context = context

    async def create(self, entity: UsersDTO):
        try:
            mapped_entity = map_users_dto_to_dao(entity)
            await self._context.get_session.add(mapped_entity)
            await self._context.get_session.flush()

            return entity
        except IntegrityError as e:
            print(f"Duplicated primary keys while creating new user: {e}")
            raise DuplicatedPrimaryKeyError(str(e))
        except DataError as e:
            print(f"Data error while creating new user: {e}")
            raise e
        except Exception as e:
            print(f"Error creating user: {e}")
            raise e

    async def get_by_id(self, id: int):
        try:
            return await self._context.get_session.get(Users, id)
        except Exception as e:
            print(f"Error retrieving user: {e}")
            raise e

    async def get_all(self):
        try:
            result = await self._context.get_session.execute(select(Users))
            return result.all()
        except Exception as e:
            print(f"Error retrieving users: {e}")
            raise e

    async def update(self, entity: UsersDTO):
        try:
            return await self._context.get_session.merge(map_users_dto_to_dao(entity))
        except DataError as e:
            print(f"Data error while updating user: {e}")
            raise e
        except Exception as e:
            print(f"Error updating user: {e}")
            raise e

    async def delete(self, id: int):
        try:
            user = await self._context.get_session.get(Users, id)
            if user:
                await self._context.get_session.delete(user)
                return True
            raise DataError
        except Exception as e:
            print(f"Error deleting user: {e}")
            raise e
