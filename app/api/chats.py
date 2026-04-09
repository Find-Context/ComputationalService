from repository import postgres
from models import ChatsDTO
from mapper import map_chats_dto_to_dao

from fastapi import APIRouter, status

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_chat(chat_dto: ChatsDTO):
    dao = map_chats_dto_to_dao(chat_dto)
    await postgres.create_chat(dao)
