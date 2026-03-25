from repository import mongo_repository
from models import MessageDTO
from mapper import map_message_dto_to_dao

from fastapi import APIRouter, FastAPI, status

app = FastAPI()
router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_message(message: MessageDTO):
    dto = await map_message_dto_to_dao(message)
    await mongo_repository.insert_message(dto)
    return {"message": "Message inserted successfully"}


app.include_router(router)
