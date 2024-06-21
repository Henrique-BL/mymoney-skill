from typing import List, Optional
from pydantic import ValidationError

from src.models.Cell import Cell
from src.schemas.Cell import CellIn, CellOut, CellUpdateOut, CellUpdateIn
from src.repositorys.CellRepository import CellRepository


class SheetService:
    def __init__(self):
        self._repository = CellRepository()

    async def _initialize(self):
        self._repository = CellRepository()
        await self._repository.initialize()

    async def create_cell(self, cell_in: CellIn) -> Optional[CellOut]:
        try:
            # Validate the input cell using Cell schema
            data: dict = cell_in.model_dump()

            cell = Cell(**cell_in.model_dump())
            # Create a new document in the repository

            await self._repository.addCellToColumn(
                data["worksheet_name"],
                data["column_name"],
                cell.model_dump(exclude={"worksheet_name", "column_name"}),
            )

            # Validate the output cell using CellOut schema
            return CellOut(**cell.model_dump(exclude_defaults=True))

        except ValueError as e:
            # Handle validation error
            print(f"Value Error: {e}")
            return None

    async def get_cell(self, cell_in: CellIn) -> Optional[CellOut]:
        data: dict = cell_in.model_dump()
        try:
            cell_document: dict = await self._repository.getCell(
                data["worksheet_name"], data["column_name"], data["row"], data["col"]
            )
            del cell_document["created_at"]
            del cell_document["updated_at"]

            if cell_document:
                return CellOut(**cell_document)

        except ValueError as e:
            print(e)
            return None

        return None

    async def get_all_cells(
        self, worksheet_name: str, column_name: str
    ) -> List[CellOut]:
        try:
            cells = await self._repository.getColumnCells(worksheet_name, column_name)

            return [CellOut(**cell) for cell in cells]
        except ValueError as error:
            print(error)
            return None

    async def update_cell(
        self, coord: dict, cell_in: CellUpdateIn
    ) -> Optional[CellUpdateOut]:
        try:
            data: dict = cell_in.model_dump()
            # Update the document in the repository
            await self._repository.updateCellAtColumn(
                data["worksheet_name"],
                data["column_name"],
                coord["row"],
                coord["col"],
                cell_in.model_dump(
                    exclude={"worksheet_name", "column_name"}, exclude_unset=True
                ),
            )
            # Validate the output cell using CellUpdateOut schema

            return CellUpdateOut(**cell_in.model_dump(exclude_unset=True))

        except ValidationError as e:
            # Handle validation error
            print(f"Validation Error: {e}")
            return None
        except ValueError as e:
            print(f"ValueError: {e}")
            return None

    async def delete_cell(self, cell_in: CellIn) -> bool:
        try:
            await self._repository.deleteCell(
                **cell_in.model_dump(exclude={"type", "value"})
            )
            return True
        except ValueError as error:
            print(error)
            return False
