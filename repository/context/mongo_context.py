from core import settings
from . import Singleton

from pymongo import AsyncMongoClient


class Mongo(metaclass=Singleton):
    def __init__(self):
        connection = (f"mongodb://"
                      # f"{settings.mongo_user}:"
                      # f"{settings.mongo_password}@"
                      f"{settings.mongo_host}:"
                      f"{settings.mongo_port}"
                      f"/?authSource={settings.mongo_auth}"
                      )
        try:
            self._client = AsyncMongoClient(connection)
        except Exception as e:
            print(f"Error connecting to MongoDB")
            raise e
        self._database = self._client.get_database(settings.mongo_db)

    @property
    def get_database(self):
        return self._database

    def close_connection(self):
        self._client.close()


mongo = Mongo()
