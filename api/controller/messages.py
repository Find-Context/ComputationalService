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
