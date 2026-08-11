from core.dto import UsersDTO

from fastapi import APIRouter, status, Depends

from api.dependencies import get_user_service, get_users_chats_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def insert_user(user_dto: UsersDTO, service=Depends(get_user_service)):
    await service.create_user(user_dto)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, service=Depends(get_user_service)):
    user = await service.get_user_by_id(user_id)
    return {"user": user}


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_users(service=Depends(get_user_service)):
    users = await service.get_all_users()
    return {"users": users}


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_user(user_dto: UsersDTO, service=Depends(get_user_service)):
    user = await service.update_user(user_dto)
    return {"user": user}


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, service=Depends(get_user_service)):
    await service.delete_user(user_id)
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/chats/{chat_id}", status_code=status.HTTP_201_CREATED)
async def create_user_chat_connection(user_id: int, chat_id: int, service=Depends(get_users_chats_service)):
    await service.create_user_chat(user_id, chat_id)
    return {"message": "Chat connection created successfully"}


@router.get("/{user_id}/chats", status_code=status.HTTP_200_OK)
async def get_user_chat_connections(user_id: int, service=Depends(get_users_chats_service)):
    user_chats = await service.get_user_chats(user_id)
    return {"chats": user_chats}


@router.delete("/{user_id}/chats/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_user_chat_connection(user_id: int, chat_id: int, service=Depends(get_users_chats_service)):
    await service.delete_user_chat(user_id, chat_id)
    return {"message": "Chat connection deleted successfully"}
