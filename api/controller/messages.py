from domain.models import MessageDTO

from fastapi import APIRouter, status, Depends

from api.dependencies import get_message_service
router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_message(message: MessageDTO, service=Depends(get_message_service)):
    await service.create_message(message)
