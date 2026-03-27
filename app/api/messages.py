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
    except DuplicateKeyError as e:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Message with the same chatId and messageId already exists"}
    except Exception as e:
        # TODO: handle exceptions in middleware, maybe with some kind of custom exception class or something like that
        print(f"Error inserting message: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Error inserting message" + str(e)}
    return {"message": "Message inserted successfully"}