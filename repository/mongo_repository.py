from pymongo.errors import DuplicateKeyError

from repository.context.mongo_context import mongo
from models import Message


async def insert_message(message: Message):
    # TODO: implement auto parsing of message and writing to database, maybe with some kind of decorator or something like that
    try:
        await mongo.get_database.get_collection("messages").insert_one(
            message.model_dump(mode='json')
        )
    except DuplicateKeyError as e:
        print(f"Duplicate key error: {e}")
        raise e
    # TODO: handle other exceptions, maybe with some kind of custom exception class or something like that
    except Exception as e:
        print(f"Error inserting message: {e}")
        return
