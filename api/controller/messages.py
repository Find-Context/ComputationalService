from core.dto import MessageDTO

from fastapi import APIRouter, status, Depends

from api.dependencies import get_message_service

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_message(message: MessageDTO, service=Depends(get_message_service)):
    return await service.create_message(message)


@router.post("/fast_search", status_code=status.HTTP_200_OK)
async def find_by_context(message: MessageDTO, service=Depends(get_message_service)):
    message_id = await service.fast_search(message)
    return message_id


@router.get("/{message_id}", status_code=status.HTTP_200_OK)
async def get_message(message_id: int, service=Depends(get_message_service)):
    message = await service.get_message_by_id(message_id)
    return {"message": message}


@router.get("/chats/{chat_id}", status_code=status.HTTP_200_OK)
async def get_messages_by_chat(chat_id: int, service=Depends(get_message_service)):
    messages = await service.get_all_messages_by_chat(chat_id)
    return {"messages": messages}


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_message(message: MessageDTO, service=Depends(get_message_service)):
    updated = await service.update_message(message)
    return {"updated": updated}


@router.delete("/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(message_id: int, service=Depends(get_message_service)):
    deleted = await service.delete_message(message_id)
    return {"deleted": deleted}
