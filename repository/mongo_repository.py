from repository.context.mongo_context import mongo
from models import Message


async def insert_message(message: Message):
    # TODO: implement auto parsing of message and writing to database, maybe with some kind of decorator or something like that
    try:
        result = await mongo.get_database.get_collection("messages").insert_one(
            {
                "chatId": message.chat_id,
                "messageId": message.message_id,
                "type": message.type.value,
                "vector": message.vector,
                "text": message.text,
                "hasDocument": message.has_document,
                "hasAudio": message.has_audio,
                "hasPhoto": message.has_photo,
                "hasVideo": message.has_video,
                "createdAt": message.created_at
            }
        )
    except Exception as e:
        print(f"Error inserting message: {e}")
