from motor.motor_asyncio import AsyncIOMotorClient
from mymoney.contrib.settings import settings


class MongoDatabase:
    def __init__(self) -> None:
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.MONGO_URI, uuidRepresentation="standard"
        )

    def _getClient(self) -> AsyncIOMotorClient:
        return self._client


database = MongoDatabase()
