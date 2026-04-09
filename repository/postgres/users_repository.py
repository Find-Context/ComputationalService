from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions.entity_error import DuplicatedPrimaryKeyError
from ..context import _postgres_context
from models import Users, UsersChats


async def create_new_user(new_user: Users):
    async with _postgres_context.get_session() as session:
        try:
            session.add(new_user)

            await session.commit()
            await session.refresh(new_user)

            return new_user
        except IntegrityError as e:
            await session.rollback()
            print(f"Error creating user: {e}")
            raise DuplicatedPrimaryKeyError(f"User already exists.")
        except Exception as e:
            print(f"Error creating user: {e}")
            raise e


async def get_user_by_id(telegram_id: int):
    async with _postgres_context.get_session() as session:
        try:
            return await session.get(Users, telegram_id)
        except Exception as e:
            print(f"Error retrieving user: {e}")
            raise e


async def get_user_by_username(username: str):
    async with _postgres_context.get_session() as session:
        try:
            result = await session.execute(select(Users).where(Users.username == username))
            return result.scalars().first()
        except Exception as e:
            print(f"Error retrieving user: {e}")
            raise e


async def create_user_chat_connection(user_id: int, chat_id: int):
    async with _postgres_context.get_session() as session:
        try:
            user_chat = UsersChats(user_id=user_id, chat_id=chat_id)
            session.add(user_chat)
            await session.commit()
            await session.refresh(user_chat)
            return user_chat
        except IntegrityError as e:
            await session.rollback()
            print(f"Error creating user-chat connection: {e}")
            raise DuplicatedPrimaryKeyError(f"Connection between user {user_id} and chat {chat_id} already exists.")
        except Exception as e:
            print(f"Error creating user-chat connection: {e}")
            raise e
