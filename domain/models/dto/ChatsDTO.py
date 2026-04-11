from datetime import datetime

from pydantic import BaseModel


class ChatsDTO(BaseModel):
    telegram_chat_id: int
    title: str
    created_at: datetime
