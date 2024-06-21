from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
)
from src.contrib.settings import settings


class BaseMongo:
    def __init__(self) -> None:
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.MONGO_URI, uuidRepresentation="standard"
        )
        self._db = self._client[settings.MONGO_DB]
        self._collection: AsyncIOMotorCollection = self._db[settings.CURRENT_YEAR]

    def close(self):
        self._client.close()

    async def initialize(self):
        await self.create_worksheets_list()
        await self.addWorksheet()

    ##All the functions bellow are used to created the database strucutre

    async def create_worksheets_list(self) -> None:
        """
        Create a initial array of worksheets in the collection

        """
        existing_base = await self._collection.find_one(
            {"worksheets": {"$exists": True}}
        )

        if not existing_base:
            await self._collection.insert_one({"worksheets": []})

    async def addWorksheet(self) -> None:
        """
        Creates and add a worksheet with name: CURRENT_MONTH in the collection

        """
        existing_worksheet = await self._collection.find_one(
            {"worksheets.name": settings.CURRENT_MONTH}
        )
        # Adiciona uma nova worksheet se não existir para o mês atual
        if not existing_worksheet:
            await self._collection.update_one(
                {"worksheets.name": {"$ne": settings.CURRENT_MONTH}},
                {
                    "$push": {
                        "worksheets": {"name": settings.CURRENT_MONTH, "columns": []}
                    }
                },
                upsert=True,
            )

            await self.defineColumns()

    async def defineColumns(self) -> None:
        """
        Defines all headers by calling _addColumnToWorksheet() to every header
        Ex: column:[{name:"Money",data:[]}]
        """
        # Checks if columns were already created
        document = await self._collection.find_one(
            {"worksheets.name": settings.CURRENT_MONTH}, {"worksheets.$": 1}
        )
        worksheet: dict = document["worksheets"][0]

        if len(worksheet["columns"]) == len(settings.HEADERS):
            raise ValueError(
                f"All columns were created already in worksheet {worksheet['name']}"
            )

        for column in settings.HEADERS:
            await self.addColumnToWorksheet(settings.CURRENT_MONTH, column)

    async def addColumnToWorksheet(self, worksheet_name: str, column_name: str) -> None:
        """
        Creates a {} item to every header and add to the column array
        Ex: column:[{name:"Money",data:[]}]
        """
        # Adiciona um campo (column) em uma worksheet específica
        await self._collection.update_one(
            {"worksheets.name": worksheet_name},
            {"$push": {"worksheets.$.columns": {"name": column_name, "data": []}}},
        )
