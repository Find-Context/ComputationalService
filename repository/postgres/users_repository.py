from datetime import datetime

from sqlalchemy import select
from ..context import postgres
from models import Users


async def create_new_user(telegram_id: int, username: str, first_name: str, last_name: str):
    async with postgres.get_session() as session:
        new_user = Users(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            registered_at=datetime.now()
        )

        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user


async def get_user_by_telegram_id(telegram_id: int):
    async with postgres.get_session() as session:
        return await session.get(Users, telegram_id)


async def get_user_by_username(username: str):
    async with postgres.get_session() as session:
        result = await session.execute(select(Users).where(Users.username == username))
        return result.scalars().first()
