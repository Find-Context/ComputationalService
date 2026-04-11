from datetime import datetime

from pydantic import BaseModel

from core import MessageTypes


class MessageDTO(BaseModel):
    chat_id: int
    message_id: int
    type: MessageTypes
    vector: list
    text: str
    created_at: datetime
