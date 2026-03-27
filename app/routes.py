from fastapi import APIRouter

from app.api import messages

api_router = APIRouter()
api_router.include_router(messages.router)
