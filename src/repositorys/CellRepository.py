from typing import Dict, List, Optional

from src.database.BaseMongo import BaseMongo


class CellRepository(BaseMongo):
    def __init__(self) -> None:
        super().__init__()

    async def checkCellExistence(self, worksheet_name: str, row: int, col: int):
        existing_field = await self._collection.find_one(
            {
                "worksheets": {
                    "$elemMatch": {
                        "name": worksheet_name,
                        "columns": {
                            "$elemMatch": {
                                # "name": column_name,
                                # takes column name in consideration
                                "data": {"$elemMatch": {"row": row, "col": col}}
                            }
                        },
                    }
                }
            }
        )
        return existing_field

    async def addCellToColumn(
        self, worksheet_name: str, column_name: str, field_value: Dict
    ):
        # Verificar se a combinação de row e col já existe na coluna do mesmo worksheet
        existing_field = await self.checkCellExistence(
            worksheet_name, field_value["row"], field_value["col"]
        )

        if existing_field is not None:
            raise ValueError(
                f"The combination of {field_value['row']} an col {field_value['col']}\
                already exists in {column_name} of worksheet {worksheet_name}."
            )

        # Adicionar o novo field_value se a combinação for única no mesmo worksheet
        result = await self._collection.update_one(
            {"worksheets.name": worksheet_name, "worksheets.columns.name": column_name},
            {"$push": {"worksheets.$[worksheet].columns.$[column].data": field_value}},
            array_filters=[
                {"worksheet.name": worksheet_name},
                {"column.name": column_name},
            ],
        )

        if result.modified_count == 0:
            raise ValueError(
                f"The field with row {field_value['row']}\
                    and col {field_value['col']} in column \
                    {column_name} of worksheet {worksheet_name}\
                        was not found or the value is the same."
            )

        return result

    async def updateCellAtColumn(
        self, worksheet_name: str, column_name: str, row: int, col: int, new_data: Dict
    ):
        try:
            # Check field existence
            cell_data: dict = await self.getCell(worksheet_name, column_name, row, col)

            # If the new_data coords were altered,
            # checks if any field already exists at those
            if (
                new_data["row"] != cell_data["row"]
                or new_data["col"] != cell_data["col"]
            ):
                existing_field = await self.checkCellExistence(
                    worksheet_name, new_data["row"], new_data["col"]
                )

                if existing_field is not None:
                    raise ValueError(
                        f"The combination of row {new_data['row']}\
                            and col {new_data['col']} \
                            already exists in {column_name}\
                            of worksheet {worksheet_name}."
                    )

            # delete cell['created_at'] bc it wont participate in the update
            del cell_data["created_at"]
            # Copy new_data new values into cell_data dict
            for key, value in new_data.items():
                if new_data[key] != cell_data[key]:
                    cell_data[key] = new_data[key]

        except ValueError as error:
            raise error

        # Updates the value of a specific field in a column
        result = await self._collection.update_one(
            {
                "worksheets.name": worksheet_name,
                "worksheets.columns.name": column_name,
                "worksheets.columns.data.row": row,
                "worksheets.columns.data.col": col,
            },
            {
                "$set": {
                    "worksheets.$[worksheet].columns.$[column].data.$[elem]": cell_data
                }
            },
            array_filters=[
                {"worksheet.name": worksheet_name},
                {"column.name": column_name},
                {"elem.row": row, "elem.col": col},
            ],
        )
        if result.modified_count == 0:
            raise ValueError(
                f"The field with row {row} and col {col} in column {column_name}\
                    of worksheet {worksheet_name} value is the same."
            )

        print(
            f"Field with row {row} and col {col} in column {column_name}\
                of worksheet {worksheet_name} updated successfully."
        )

    async def deleteCell(
        self, worksheet_name: str, column_name: str, row: int, col: int
    ) -> None:
        # Usar $pull para remover o item específico de data[]
        result = await self._collection.update_one(
            {"worksheets.name": worksheet_name, "worksheets.columns.name": column_name},
            {
                "$pull": {
                    "worksheets.$[worksheet].columns.$[column].data": {
                        "row": row,
                        "col": col,
                    }
                }
            },
            array_filters=[
                {"worksheet.name": worksheet_name},
                {"column.name": column_name},
            ],
        )

        if result.modified_count == 0:
            raise ValueError(
                f"The item at {row} an col {col}\
                    wasnt found {column_name} in worksheet {worksheet_name}."
            )

        print(
            f"Item with row {row} and col {col} remove sucessfuly of column\
                {column_name} at worksheet {worksheet_name}."
        )

    async def getCell(
        self, worksheet_name: str, column_name: str, row: int, col: int
    ) -> Optional[Dict]:
        # Buscar o field_value que corresponde à combinação
        # de row e col em uma coluna específica
        try:
            data: List[dict] = await self.getColumnCells(worksheet_name, column_name)

        except ValueError as e:
            raise e
        # Encontrar e retornar o field_value específico dentro da coluna
        if data:
            for field in data:
                if field.get("row") == row and field.get("col") == col:
                    return field
        raise ValueError(f"The field in {column_name} at row:{row} was not found")

    async def getColumnCells(
        self, worksheet_name: str, column_name: str
    ) -> Optional[List]:
        document = await self._collection.find_one(
            {"worksheets.name": worksheet_name, "worksheets.columns.name": column_name},
            {"worksheets.$": 1},
        )
        if not document:
            raise ValueError(
                f"The column {column_name} of worksheet\
                    {worksheet_name} was not found. "
            )

        if document:
            worksheet: dict = document["worksheets"][0]

            # Search for column data, return dict of data (row, col, value, type)
            # or none if data is empty
            for column in worksheet.get("columns"):
                if column["name"] == column_name:
                    if column["data"]:
                        return column["data"]
