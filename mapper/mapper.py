from models import MessageDTO, Message
from core import MessageTypes


async def map_message_dto_to_dao(message_dto: MessageDTO) -> Message:
    message_dao = Message(
        chat_id=message_dto.chat_id,
        message_id=message_dto.message_id,
        type=message_dto.type,
        vector=message_dto.vector,
        text=message_dto.text,
        has_document=True if message_dto.type == MessageTypes.DOCUMENT else False,
        has_audio=True if message_dto.type == MessageTypes.AUDIO else False,
        has_photo=True if message_dto.type == MessageTypes.IMAGE else False,
        has_video=True if message_dto.type == MessageTypes.VIDEO else False,
        created_at=message_dto.created_at
    )

    return message_dao
