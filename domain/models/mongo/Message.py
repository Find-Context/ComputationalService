from datetime import datetime

from pydantic import BaseModel

from core import MessageTypes


class Message(BaseModel):
    chat_id: int
    message_id: int
    type: MessageTypes
    vector: list
    text: str
    has_document: bool = False
    has_audio: bool = False
    has_photo: bool = False
    has_video: bool = False
    created_at: datetime
