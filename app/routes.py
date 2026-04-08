from fastapi import APIRouter

from app.api import messages

message_router = APIRouter()
message_router.include_router(messages.router)
