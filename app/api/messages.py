from repository import message_repository
from models import MessageDTO
from mapper import map_message_dto_to_dao

from fastapi import APIRouter, status

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_message(message: MessageDTO):
    dao = map_message_dto_to_dao(message)
    await message_repository.insert_message(dao)
