from datetime import datetime

from ..context import _postgres_context
from models import Chats


async def create_chat(new_chat: Chats):
    async with _postgres_context.get_session() as session:
        session.add(new_chat)

        await session.commit()
        await session.refresh(new_chat)
        return new_chat


async def get_chat(telegram_chat_id: int):
    async with _postgres_context.get_session() as session:
        return await session.get(Chats, telegram_chat_id)
