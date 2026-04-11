from domain import UsersService, ChatsService, UsersChatsService, MessageService
from infrastructure.repository import UsersRepository, ChatsRepository, UsersChatsRepository, MessageRepository
from infrastructure.repository.context import _postgres_context, _mongo_context


async def get_user_service():
    async with _postgres_context.get_session as session:
        user_repo = UsersRepository(session)

        try:
            yield UsersService(user_repo)
            await session.commit()
        except Exception as e:
            print(f"Error in user service dependency: {e}")
            await session.rollback()
            raise e


async def get_chat_service():
    async with _postgres_context.get_session as session:
        chat_repo = ChatsRepository(session)

        try:
            yield ChatsService(chat_repo)
            await session.commit()
        except Exception as e:
            print(f"Error in chat service dependency: {e}")
            await session.rollback()
            raise e


async def get_users_chats_service():
    async with _postgres_context.get_session as session:
        users_chats_repo = UsersChatsRepository(session)

        try:
            yield UsersChatsService(users_chats_repo)
            await session.commit()
        except Exception as e:
            print(f"Error in users-chats service dependency: {e}")
            await session.rollback()
            raise e


async def get_message_service():
    mongo_repo = MessageRepository(_mongo_context)
    try:
        yield MessageService(mongo_repo)
    except Exception as e:
        print(f"Error in message service dependency: {e}")
        raise e
