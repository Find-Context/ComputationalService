from repository import postgres
from models import UsersDTO
from mapper import map_users_dto_to_dao

from fastapi import APIRouter, status

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def insert_user(user_dto: UsersDTO):
    dao = map_users_dto_to_dao(user_dto)
    await postgres.create_new_user(dao)
    return {"message": "User created successfully"}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    user = await postgres.get_user_by_id(user_id)
    return {"user": user}


@router.post("/{user_id}/chats/{chat_id}", status_code=status.HTTP_201_CREATED)
async def create_user_chat_connection(user_id: int, chat_id: int):
    await postgres.create_user_chat_connection(user_id, chat_id)
    return {"message": "Chat connection created successfully"}
