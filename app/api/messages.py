from pymongo.errors import DuplicateKeyError

from repository import mongo_repository
from models import MessageDTO
from mapper import map_message_dto_to_dao

from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_message(message: MessageDTO, response: Response):
    try:
        dto = map_message_dto_to_dao(message)
        await mongo_repository.insert_message(dto)
    except Exception as e:
        print(f"Error inserting message: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Error inserting message" + str(e)}
    return {"message": "Message inserted successfully"}