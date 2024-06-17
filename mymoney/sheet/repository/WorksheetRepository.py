import json
from mymoney.sheet.repository.BaseRepository import BaseRepository
from gspread.cell import Cell
from gspread.worksheet import Worksheet
from mymoney.contrib import settings

from mymoney.sheet.MetadataUtil import MetadataUtil
from mymoney.sheet.exceptions.Exceptions import EmptyColumnException


class WorksheetRepository(BaseRepository):
    def __init__(self, worksheet: Worksheet) -> None:
        super().__init__()
        self._worksheet: Worksheet = worksheet

    def _initialize(self) -> bool:
        """
        Initializes the worksheet fields and defines metadata and headers.

        Returns:
            bool: True if initialization is successful.
        """
        self._defineHeaders()
        metadata: dict = self._defineMetadata()

        metadata["Created"] = True

        self._updateMetadata(metadata=metadata)

        return True

    def _insertCell(self, data: float, type: str, column: str) -> Cell:
        """
        Inserts a new cell with data and updates the corresponding type cell.

        Args:
            data (float): The financial data to insert.
            type (str): The type of transaction ("Income" or "Outcome").
            column (str): The column name (e.g., "Money", "Pix").

        Returns:
            Cell: The inserted cell.
        """
        metadata: dict = self._getMetadata()
        col: dict = metadata.get(column)
        row: int = col.get("last")

        self._worksheet.update_cell(row=row, col=col.get("index"), value=data)
        self._worksheet.update_cell(row=row, col=col.get("index") + 1, value=type)

        cell: Cell = self._searchCell(row=row, col=col.get("index"))

        col["last"] = row + 1
        self._updateMetadata(metadata=metadata, type=type, value=data)

        return cell

    def _searchCell(self, row: int, col: int) -> Cell | None:
        """
        Searches for a cell at the specified row and column.

        Args:
            row (int): The row number.
            col (int): The column number.

        Returns:
            Cell: The cell object.
            None: Cell empty
        """
        cell: Cell = self._worksheet.cell(row=row, col=col)

        return cell

    def _deleteLastCell(self, column: str) -> None:
        """
        Deletes the last cell in the specified column and updates metadata.

        Args:
            column (str): The column name (e.g., "Money", "Pix").
        """
        metadata: dict = self._getMetadata()
        col: dict = metadata.get(column)
        row: int = col.get("last")

        if row - 1 == settings.HEADERS_DEFAULT_ROW:
            raise EmptyColumnException(column)

        cell: Cell = self._searchCell(row=row - 1, col=col.get("index"))

        type_cell: Cell = self._searchCell(row=row - 1, col=cell.col + 1)

        metadata[type_cell.value] -= cell.numeric_value
        col["last"] = (
            col["last"] - 1
            if col["last"] > settings.DATA_ROW_DEFAULT
            else settings.DATA_ROW_DEFAULT
        )

        cell.value = ""
        type_cell.value = ""

        self._worksheet.update_cells([cell, type_cell])
        self._updateMetadata(metadata=metadata)

    def _defineHeaders(self) -> None:
        """
        Defines the headers for the spreadsheet if they are not already present.
        """
        headers: list[str] = settings.HEADERS
        # Verify if headers already exist
        if not headers == self._worksheet.row_values(settings.HEADERS_DEFAULT_ROW):
            self._worksheet.insert_row(headers, settings.HEADERS_DEFAULT_ROW)
        else:
            print("\n Exception: Header already defined")

    def _defineMetadata(self) -> dict:
        """
        Retrieves metadata from the first cell (settings.DEFAULT) and \
            converts it to a dictionary.

        Returns:
            dict: The metadata dictionary.
        """

        metadata: dict = MetadataUtil.defaultMetadata()
        self._worksheet.update_acell(
            settings.METADATA_DEFAULT_INDEX, json.dumps(metadata)
        )

        return self._getMetadata()

    def _getMetadata(self) -> dict:
        """
        Retrieves metadata from the first cell (A1) and converts it to a dictionary.

        Returns:
            dict: The metadata dictionary.
        """
        data: Cell = self._worksheet.acell(settings.METADATA_DEFAULT_INDEX).value
        metadata: dict = json.loads(data)
        return metadata

    def _updateMetadata(
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
