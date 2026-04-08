from repository import postgres
from models import UsersDTO
from mapper import map_users_dto_to_dao

from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def insert_user(user_dto: UsersDTO, response: Response):
    try:
        dao = map_users_dto_to_dao(user_dto)
        await postgres.insert_user(dao)
    except Exception as e:
        print(f"Error inserting user: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Error inserting user" + str(e)}
    return {"message": "User inserted successfully"}
