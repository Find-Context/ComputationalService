from domain import UsersService, ChatsService, UsersChatsService, MessageService
from infrastructure.repository import UsersRepository, ChatsRepository, UsersChatsRepository, MessageRepository
from infrastructure.repository.context import _postgres_context, _mongo_context


async def get_user_service():
    user_repo = UsersRepository(_postgres_context)

    yield UsersService(user_repo)
    await _postgres_context.get_session.commit()


async def get_chat_service():
    chat_repo = ChatsRepository(_postgres_context)

    yield ChatsService(chat_repo)
    await _postgres_context.get_session.commit()


async def get_users_chats_service():
    users_chats_repo = UsersChatsRepository(_postgres_context)

    yield UsersChatsService(users_chats_repo)
    await _postgres_context.get_session.commit()


async def get_message_service():
    mongo_repo = MessageRepository(_mongo_context)

    yield MessageService(mongo_repo)
