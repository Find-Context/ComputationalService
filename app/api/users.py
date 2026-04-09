from repository import postgres
from models import UsersDTO
from mapper import map_users_dto_to_dao

from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def insert_user(user_dto: UsersDTO, response: Response):
    try:
        dao = map_users_dto_to_dao(user_dto)
        await postgres.create_new_user(dao)
    except Exception as e:
        print(f"Error inserting user: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Error inserting user" + str(e)}
    return {"message": "User inserted successfully"}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, response: Response):
    try:
        user = await postgres.get_user_by_id(user_id)
        if not user:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "User not found"}
    except Exception as e:
        print(f"Error retrieving user: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Error retrieving user" + str(e)}
    return user


@router.post("/{user_id}/chats/{chat_id}", status_code=status.HTTP_201_CREATED)
async def create_user_chat_connection(user_id: int, chat_id: int, response: Response):
    try:
        await postgres.create_user_chat_connection(user_id, chat_id)
    except Exception as e:
        print(f"Error creating user-chat connection: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Error creating user-chat connection" + str(e)}
    return {"message": "User-chat connection created successfully"}
