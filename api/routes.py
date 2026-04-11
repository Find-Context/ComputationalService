from fastapi import APIRouter

from api.controller import users, messages, chats

api_router = APIRouter()
api_router.include_router(messages.router)
api_router.include_router(users.router)
api_router.include_router(chats.router)
