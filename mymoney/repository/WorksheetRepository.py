import json
from mymoney.repository.BaseRepository import BaseRepository
from gspread.cell import Cell
from gspread.client import Client
from gspread.worksheet import Worksheet
from mymoney.contrib import settings

from mymoney.utils.MetadataUtil import MetadataUtil


class WorksheetRepository(BaseRepository):
    def __init__(self, client: Client) -> None:
        super().__init__(client=client)
        self._worksheet: Worksheet = None

    def setWorkheet(self, worksheet: Worksheet):
        self._worksheet = worksheet

    def initialize(self) -> bool:
        """
        Initializes the worksheet fields and defines metadata and headers.

        Returns:
            bool: True if initialization is successful.
        """
        self.defineHeaders()
        metadata = self.defineMetadata()

        metadata["Created"] = True

        self.updateMetadata(metadata=metadata)

        return True

    def defineMetadata(self) -> dict:
        """
        Retrieves metadata from the first cell (settings.DEFAULT) and \
            converts it to a dictionary.

        Returns:
            dict: The metadata dictionary.
        """

        metadata = MetadataUtil.defaultMetadata()
        self._worksheet.update_acell(
            settings.METADATA_DEFAULT_INDEX, json.dumps(metadata)
        )

        return self.getMetadata()

    def defineHeaders(self) -> None:
        """
        Defines the headers for the spreadsheet if they are not already present.
        """
        headers = settings.HEADERS
        # Verify if headers already exist
        breakpoint()
        if not headers == self._worksheet.row_values(settings.HEADERS_DEFAULT_ROW):
            self._worksheet.insert_row(headers, settings.HEADERS_DEFAULT_ROW)
        else:
            print("\n Exception: Header already defined")

    def insertCell(self, data: float, type: str, column: str) -> Cell:
        """
        Inserts a new cell with data and updates the corresponding type cell.

        Args:
            data (float): The financial data to insert.
            type (str): The type of transaction ("Income" or "Outcome").
            column (str): The column name (e.g., "Money", "Pix").

        Returns:
            Cell: The inserted cell.
        """
        metadata = self.getMetadata()
        col: dict = metadata.get(column)
        row = col.get("last")

        self._worksheet.update_cell(row=row, col=col.get("index"), value=data)
        self._worksheet.update_cell(row=row, col=col.get("index") + 1, value=type)

        cell = self.searchCell(row=row, col=col.get("index"))

        col["last"] = row + 1
        self.updateMetadata(metadata=metadata, type=type, value=data)

        return cell

    def deleteLastCell(self, column: str) -> None:
        """
        Deletes the last cell in the specified column and updates metadata.

        Args:
            column (str): The column name (e.g., "Money", "Pix").
        """
        metadata = self.getMetadata()
        col: dict = metadata.get(column)
        row = col.get("last")

        cell = self.searchCell(row=row - 1, col=col.get("index"))
        type_cell = self.searchCell(row=row - 1, col=cell.col + 1)

        metadata[type_cell.value] -= cell.numeric_value
        col["last"] = (
            col["last"] - 1
            if col["last"] > settings.DATA_ROW_DEFAULT
            else settings.DATA_ROW_DEFAULT
        )

        cell.value = ""
        type_cell.value = ""

        self._worksheet.update_cells([cell, type_cell])
        self.updateMetadata(metadata=metadata)

    def searchCell(self, row: int, col: int) -> Cell:
        """
        Searches for a cell at the specified row and column.

        Args:
            row (int): The row number.
            col (int): The column number.

        Returns:
            Cell: The cell object.
        """
        cell: Cell = self._worksheet.cell(row=row, col=col)

        return cell

    def getMetadata(self) -> dict:
        """
        Retrieves metadata from the first cell (A1) and converts it to a dictionary.

        Returns:
            dict: The metadata dictionary.
        """
        data = self._worksheet.acell(settings.METADATA_DEFAULT_INDEX).value
        metadata = json.loads(data)
        return metadata

    def updateMetadata(
        self, metadata: dict, type: str = None, value: float = None
    ) -> None:
        """
        Updates the metadata in cell A1 after insert, update, or delete actions.

        Args:
            metadata (dict): The metadata dictionary.
            type (str | None): The type of transaction ("Income" or "Outcome").
            value (float | None): The transaction amount.
        """

        if type == "Income":
            metadata["Income"] += value
        elif type == "Outcome":
            metadata["Outcome"] += value

        self._worksheet.update_acell(
            settings.METADATA_DEFAULT_INDEX, json.dumps(metadata)
        )
