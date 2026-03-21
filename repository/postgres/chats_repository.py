from datetime import datetime

from ..context import postgres
from models import Chats


async def create_chat(telegram_chat_id: int, title: str):
    async with postgres.get_session() as session:
        new_chat = Chats(
            telegram_chat_id=telegram_chat_id,
            title=title,
            created_at=datetime.now()
        )
        session.add(new_chat)

        await session.commit()
        await session.refresh(new_chat)
        return new_chat


async def get_chat(telegram_chat_id: int):
    async with postgres.get_session() as session:
        return await session.get(Chats, telegram_chat_id)
