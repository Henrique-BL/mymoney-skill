from typing import List, Optional
from uuid import UUID
from pydantic import ValidationError

from mymoney.models.Data import Data
from mymoney.schemas.Data import DataIn, DataOut, DataUpdateOut, DataUpdate
from mymoney.repositorys.DataRepository import DataRepository


class DataService:
    def __init__(self):
        self.repository = DataRepository()

    async def initialize(self):
        self.repository = DataRepository()
        await self.repository.create_indexes()

    async def create_data(self, data_in: DataIn) -> DataOut:
        try:
            # Validate the input data using DataIn schema
            Data.model_validate(data_in)
            # Create a new document in the repository
            created_data: dict = await self.repository.create(data_in)

            # Validate the output data using DataOut schema
            return DataOut(**created_data)

        except ValidationError as e:
            # Handle validation error
            print(f"Validation Error: {e}")
            raise e

    async def get_data_by_id(self, data_id: UUID) -> Optional[DataOut]:
        data_document = await self.repository.read_by_id(data_id)
        if data_document:
            return DataOut(**data_document)
        return None

    async def get_all_data(self) -> List[DataOut]:
        documents = await self.repository.read_all()
        return [DataOut(**doc) for doc in documents]

    async def update_data(
        self, data_id: UUID, data_in: DataUpdate
    ) -> Optional[DataUpdateOut]:
        try:
            DataUpdate.model_validate(data_in)
            # Update the document in the repository
            updated_data = await self.repository.update(data_id, data_in)
            del updated_data["_id"]
            if updated_data:
                # Validate the output data using DataUpdateOut schema
                return DataUpdateOut(**updated_data)

            return None

        except ValidationError as e:
            # Handle validation error
            print(f"Validation Error: {e}")
            raise e

    async def delete_data(self, data_id: UUID) -> bool:
        return await self.repository.delete(data_id)

    async def search(self, row: int, column: int) -> UUID:
        cell = await self.repository.searchCell(row=row, col=column)
        return cell["id"]
