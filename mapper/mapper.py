from models import MessageDTO, Message
from core import MessageTypes


def map_message_dto_to_dao(message_dto: MessageDTO) -> Message:
    message_type = message_dto.type

    message_dao = Message(
        chat_id=message_dto.chat_id,
        message_id=message_dto.message_id,
        type=message_type,
        vector=message_dto.vector,
        text=message_dto.text,
        has_document=message_type == MessageTypes.DOCUMENT,
        has_audio=message_type == MessageTypes.AUDIO,
        has_photo=message_type == MessageTypes.IMAGE,
        has_video=message_type == MessageTypes.VIDEO,
        created_at=message_dto.created_at,
    )

    return message_dao
