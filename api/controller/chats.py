from core.dto import ChatsDTO

from fastapi import APIRouter, status, Depends

from api.dependencies import get_chat_service, get_hybrid_repository
router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_chat(chat_dto: ChatsDTO, service=Depends(get_chat_service)):
    await service.create_chat(chat_dto)


@router.get("/{chat_id}", status_code=status.HTTP_200_OK)
async def get_chat(chat_id: int, service=Depends(get_chat_service)):
    chat = await service.get_chat_by_id(chat_id)
    return {"chat": chat}


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_chats(service=Depends(get_chat_service)):
    chats = await service.get_all_chats()
    return {"chats": chats}


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_chat(chat_dto: ChatsDTO, service=Depends(get_chat_service)):
    chat = await service.update_chat(chat_dto)
    return {"chat": chat}


@router.delete("/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_chat(chat_id: int, service=Depends(get_chat_service)):
    await service.delete_chat(chat_id)
    return {"message": "Chat deleted successfully"}


@router.get("/{chat_id}/context", status_code=status.HTTP_200_OK)
async def get_chat_context(chat_id: int, repository=Depends(get_hybrid_repository)):
    return await repository.get_chat_with_messages(chat_id)
