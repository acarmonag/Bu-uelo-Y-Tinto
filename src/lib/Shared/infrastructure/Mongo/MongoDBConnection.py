from typing import AsyncGenerator, Any
from mongoengine import connect, disconnect
from config.config import Config


class MongoDBConnection:
    def __init__(self, config: Config):
        self._config = config
        self._client = None

    def connect(self):
        if not self._client:
            self._client = connect(
                db=self._config.mongo_name,
                host=self._config.mongo_host,
                alias="default",
            )
        return self._client

    def disconnect(self):
        if self._client:
            disconnect(alias="default")
            self._client = None
