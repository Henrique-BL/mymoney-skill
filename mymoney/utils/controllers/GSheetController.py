from gspread.spreadsheet import Spreadsheet
from gspread.cell import Cell
from gspread.client import Client
from mymoney.contrib import settings
from mymoney.utils.controllers.SpreadsheetController import SpreadsheetController
from mymoney.utils.controllers.MetadataController import MetadataController


class GSheetController:
    """

    Attributes:
        _client: The client for interacting with Google Sheets.
        _spreadsheet: The spreadsheet object.
        _worksheet: The current worksheet
    """

    def __init__(self, client: Client) -> None:
        """
        Initializes the SheetController with the specified
        spreadsheet name and GspreadClient.

        Args:
            spreadsheet (str): The name of the spreadsheet.
            client (GspreadClient): The client to interact with Google Sheets.

        """
        self._client: Client = client
        self._spreadsheet: None
        # Default worksheet to current month
        """        try:
            self._worksheet: Worksheet = self._spreadsheet.worksheet(
                settings.CURRENT_MONTH
            )
        except WorksheetNotFound:
            self._worksheet: Worksheet = self._spreadsheet.add_worksheet(
                settings.CURRENT_MONTH
            )"""

    def initialize(self) -> bool:
        """
        Initializes the spreadsheet fields and defines metadata and headers.

        Returns:
            bool: True if initialization is successful.
        """
        MetadataController.defineMetadata(worksheet=self._worksheet)

        self.defineHeaders()

        metadata = MetadataController.getMetadata(worksheet=self._worksheet)
        metadata["Created"] = True

        MetadataController.updateMetadata(
            worksheet=self._worksheet, metadata=metadata, type=None, value=None
        )

        return True

    def setSpreadsheet(self, spreadsheet: Spreadsheet):
        self._spreadsheet = spreadsheet

    def defineHeaders(self) -> None:
        """
        Defines the headers for the spreadsheet if they are not already present.
        """
        headers = settings.HEADERS
        # Verify if headers already exist
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
        metadata = MetadataController.getMetadata(self._worksheet)
        col: dict = metadata.get(column)
        row = col.get("last")

        self._worksheet.update_cell(row=row, col=col.get("index"), value=data)
        self._worksheet.update_cell(row=row, col=col.get("index") + 1, value=type)

        cell = self.searchCell(row=row, col=col.get("index"))

        col["last"] = row + 1
        MetadataController.updateMetadata(
            worksheet=self._worksheet, metadata=metadata, type=type, value=data
        )

        return cell

    def deleteLastCell(self, column: str) -> None:
        """
        Deletes the last cell in the specified column and updates metadata.

        Args:
            column (str): The column name (e.g., "Money", "Pix").
        """
        metadata = MetadataController.getMetadata(self._worksheet)
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
        MetadataController.updateMetadata(
            worksheet=self._worksheet, metadata=metadata, type=None, value=None
        )

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

    def newSpreadsheet(self, title: str, folder_id: str) -> str:
        id = SpreadsheetController.createSpreadsheet(
            gspread=self._client, title=title, folder_id=folder_id
        )
        return id

    def deleteSpreadsheet(self, title: str, folder_id: str) -> str:
        id = SpreadsheetController.deleteSpreadsheet(
            gspread=self._client, title=title, folder_id=folder_id
        )
        return id
