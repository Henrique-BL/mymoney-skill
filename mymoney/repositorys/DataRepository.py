from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorCursor,
)
from typing import List, Optional
from uuid import UUID

from pymongo import ASCENDING, IndexModel
from mymoney.contrib.settings import settings
from mymoney.database.mongo import database
from mymoney.schemas.Data import DataIn, DataUpdate


class DataRepository:
    def __init__(self) -> None:
        self._client: AsyncIOMotorClient = database._getClient()
        self._db = self._client[settings.MONGO_DB]

        self.data_collection: AsyncIOMotorCollection = self._db[
            settings.CURRENT_COLLECTION
        ]

    async def create_indexes(self):
        # Cria um índice composto único em (row, col)
        index_model = IndexModel([("row", ASCENDING), ("col", ASCENDING)], unique=True)
        await self._db.get_collection(settings.CURRENT_COLLECTION).create_indexes(
            [index_model]
        )

    async def create(self, data: DataIn) -> dict:
        """
        Create a new Data document.
        """
        await self.data_collection.insert_one(data.model_dump())

        return data.model_dump()

    async def read_by_id(self, data_id: UUID) -> Optional[dict]:
        """
        Read a Data document by its ID.
        """
        document = await self.data_collection.find_one({"id": data_id})
        return document

    async def read_all(self) -> List[dict]:
        """
        Read all Data documents.
        """
        documents = []
        cursor: AsyncIOMotorCursor = self.data_collection.find()
        async for document in cursor:
            documents.append(document)
        return documents

    async def update(self, data_id: UUID, data_in: DataUpdate) -> Optional[dict]:
        """
        Update a Data document by its ID.

        """
        result = await self.data_collection.update_one(
            {"id": data_id}, {"$set": data_in.model_dump(exclude_unset=True)}
        )
        if result.matched_count:
            return await self.read_by_id(data_id)
        return None

    async def delete(self, data_id: UUID) -> bool:
        """
        Delete a Data document by its ID.
        """
        result = await self.data_collection.delete_one({"id": data_id})
        return result.deleted_count > 0

    async def searchCell(self, row: int, col: int) -> Optional[dict]:
        document = await self.data_collection.find_one({"row": row, "col": col})
        return document
