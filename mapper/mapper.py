from models import MessageDTO, UsersDTO, ChatsDTO, Message, Users, Chats
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


def map_users_dto_to_dao(users_dto: UsersDTO) -> Users:
    user_dao = Users(
        telegram_id=users_dto.telegram_id,
        username=users_dto.username,
        first_name=users_dto.first_name,
        last_name=users_dto.last_name,
        registered_at=users_dto.registered_at
    )

    return user_dao


def map_chats_dto_to_dao(chats_dto: ChatsDTO) -> Chats:
    chat_dao = Chats(
        telegram_chat_id=chats_dto.telegram_chat_id,
        title=chats_dto.title,
        created_at=chats_dto.created_at
    )

    return chat_dao
