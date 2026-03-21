from datetime import datetime

from repository.context.mongo_context import mongo
from core import MessageTypes


async def insert_message(chat_id: int,
                         message_id: int,
                         type: MessageTypes,
                         vector: list,
                         text: str,
                         has_document: bool = False,
                         has_audio: bool = False,
                         has_photo: bool = False,
                         has_video: bool = False
                         ):
    try:
        result = await mongo.get_database.get_collection("messages").insert_one(
            {
                "chatId": chat_id,
                "messageId": message_id,
                "type": type.value,
                "vector": vector,
                "text": text,
                "hasDocument": has_document,
                "hasAudio": has_audio,
                "hasPhoto": has_photo,
                "hasVideo": has_video,
                "createdAt": datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        return result
    except Exception as e:
        print(f"Error inserting message: {e}")
