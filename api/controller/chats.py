from core.dto import ChatsDTO

from fastapi import APIRouter, status, Depends

from api.dependencies import get_chat_service
router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_chat(chat_dto: ChatsDTO, service=Depends(get_chat_service)):
    await service.create_chat(chat_dto)
