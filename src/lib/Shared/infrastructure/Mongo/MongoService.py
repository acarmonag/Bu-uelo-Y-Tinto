from typing import Annotated

from fastapi import Depends
from mongoengine import connect

from config.config import Config, get_config
from lib.Client.infrastructure.Mongo.ClientMongoRepository import ClientMongoRepository


class MongoService:
    _instance = None

    def __init__(self, config: Config):
        self._config = config
        self._client = connect(
            host=self._config.mongo_url,
            alias="default",
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            retryWrites=True,
            retryReads=True,
        )

    @classmethod
    def get_instance(cls) -> "MongoService":
        if cls._instance is None:
            cls._instance = cls(get_config())
        return cls._instance

    def disconnect(self):
        from mongoengine import disconnect
        disconnect()


def get_mongo_service(config: Config = Depends(get_config)) -> MongoService:
    return MongoService.get_instance()


async def get_repository(
        mongo_service: Annotated[MongoService, Depends(get_mongo_service)]
) -> ClientMongoRepository:
    return ClientMongoRepository()
