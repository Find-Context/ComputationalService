from repository import postgres
from models import ChatsDTO
from mapper import map_chats_dto_to_dao

from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_chat(chat_dto: ChatsDTO, response: Response):
    try:
        dao = map_chats_dto_to_dao(chat_dto)
        await postgres.create_chat(dao)
    except Exception as e:
        print(f"Error inserting chat: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Error inserting chat" + str(e)}
    return {"message": "Chat inserted successfully"}