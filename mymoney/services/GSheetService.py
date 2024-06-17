from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from gspread.cell import Cell
from gspread.exceptions import SpreadsheetNotFound

from mymoney.sheet.repository.SpreadsheetRepository import SpreadsheetRepository
from mymoney.sheet.repository.WorksheetRepository import WorksheetRepository
from mymoney.sheet.exceptions.Exceptions import (
    FileAlreadyExistsException,
    FileNotFoundException,
)


class GSheetService:
    """

    Attributes:
        _client: The client for interacting with Google Sheets.
        _spreadsheet: The spreadsheet object.
        _worksheet: The current worksheet
    """

    def __init__(self) -> None:
        """
        Initializes the SheetController with the specified
        spreadsheet name and GspreadClient.

        Args:
            spreadsheet (str): The name of the spreadsheet.
            client (GspreadClient): The client to interact with Google Sheets.

        """

        self._spreadsheet: SpreadsheetRepository = SpreadsheetRepository()
        self._worksheet: WorksheetRepository = None
        self._currentSpreadsheet: Spreadsheet = None

    def _setCurrentSpreadsheet(self, spreadsheet: Spreadsheet) -> None:
        self._currentSpreadsheet = spreadsheet

    def _setWorksheet(self, worksheet: Worksheet) -> None:
        self._worksheet = WorksheetRepository(worksheet)

    def _newSpreadsheet(self, title: str, folder_id: str) -> str:
        """
        Creates a spreadsheet at given folder.

        Args:
            title (str): The spreadsheet title.
            folder_id (str): The destination folder_id number.

        Returns:
            id: The id of the created spreadsheet.
        """
        try:
            id: str = self._spreadsheet._createSpreadsheet(
                title=title, folder_id=folder_id
            )

            default_spreadsheet: Spreadsheet = self._searchSpreadSheet(
                identifier=id, folder_id=folder_id, search_by="id"
            )
            default_worksheet: Worksheet = default_spreadsheet.sheet1

            self._setWorksheet(default_worksheet)
            return id
        except FileAlreadyExistsException as error:
            print(error)
            return None

    def _deleteSpreadsheet(self, title: str, folder_id: str) -> str:
        """
        Deletes a spreadsheet at given folder.

        Args:
            title (str): The spreadsheet title.
            folder_id (str): The destination folder_id number.

        Returns:
            id: The id of the deleted spreadsheet.
        """
        try:
            id: str = self._spreadsheet._deleteSpreadsheet(
                title=title, folder_id=folder_id
            )
            return id
        except FileNotFoundException() as erro:
            print(erro)
            return None

    def _updateSpreadsheet(self, title: str, new_title: str, folder_id: str) -> str:
        """
        Updates the name of a spreadsheet at given folder.

        Args:
            title (str): The spreadsheet title.
            new_title (str): The spreadsheet new title.
            folder_id (str): The destination folder_id number.

        Returns:
            id: The id of the updated spreadsheet.
        """
        try:
            id: str = self._spreadsheet._updateSpreadsheet(
                title=title, new_title=new_title, folder_id=folder_id
            )
            return id
        except FileNotFoundException as error:
            print(error)
            return None
        except FileAlreadyExistsException as error:
            print(error)
            return None

    def _searchSpreadSheet(
        self, identifier: str, folder_id: str, search_by: str = "title"
    ) -> Spreadsheet:
        """
        Search for a spreadsheet with id at given folder.

        Args:
            ididentifier (str): The spreadsheet identifier (name or id key).
            folder_id (str): The destination folder_id number.
            search_by (str): search method
        Returns:
            Spreadsheet: The gspread.Spreadsheet
        """
        try:
            spreadsheet: Spreadsheet = self._spreadsheet._searchSpreadsheet(
                identifier=identifier, folder_id=folder_id, search_by=search_by
            )

            if spreadsheet is None:
                raise SpreadsheetNotFound()
            return spreadsheet
        except SpreadsheetNotFound as error:
            print(f"Spreadsheet not found. Error: {error}")
            return None
        except ValueError as error:
            print(error)
            return None

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

        return self._insertCell(data, type, column)

        # Worksheet Services Methods

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
        return self._worksheet._searchCell(row=row, col=col)

    def _deleteLastCell(self, column: str) -> None:
        """
        Deletes the last cell in the specified column and updates metadata.

        Args:
            column (str): The column name (e.g., "Money", "Pix").
        """
        self._worksheet._deleteLastCell(column)
