from gspread.spreadsheet import Spreadsheet
from gspread.client import Client
from gspread.exceptions import SpreadsheetNotFound
from mymoney.repository.SpreadsheetRepository import SpreadsheetRepository
from mymoney.utils.exceptions.Exceptions import (
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

    def __init__(self, client: Client) -> None:
        """
        Initializes the SheetController with the specified
        spreadsheet name and GspreadClient.

        Args:
            spreadsheet (str): The name of the spreadsheet.
            client (GspreadClient): The client to interact with Google Sheets.

        """
        self._client: Client = client
        self._service: SpreadsheetRepository = SpreadsheetRepository(client=client)

    def newSpreadsheet(self, title: str, folder_id: str) -> str:
        """
        Creates a spreadsheet at given folder.

        Args:
            title (str): The spreadsheet title.
            folder_id (str): The destination folder_id number.

        Returns:
            id: The id of the created spreadsheet.
        """
        try:
            id = self._service._createSpreadsheet(title=title, folder_id=folder_id)
            return id
        except FileAlreadyExistsException as error:
            print(error)
            return None

    def deleteSpreadsheet(self, title: str, folder_id: str) -> str:
        """
        Deletes a spreadsheet at given folder.

        Args:
            title (str): The spreadsheet title.
            folder_id (str): The destination folder_id number.

        Returns:
            id: The id of the deleted spreadsheet.
        """
        try:
            id = self._service._deleteSpreadsheet(title=title, folder_id=folder_id)
            return id
        except FileNotFoundException() as erro:
            print(erro)
            return None

    def updateSpreadsheet(self, title: str, new_title: str, folder_id: str) -> str:
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
            id = self._service._updateSpreadsheet(
                title=title, new_title=new_title, folder_id=folder_id
            )
            return id
        except FileNotFoundException as error:
            print(error)
            return None
        except FileAlreadyExistsException as error:
            print(error)
            return None

    def searchSpreadSheet(
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
            spreadsheet: Spreadsheet = self._service._searchSpreadsheet(
                identifier=identifier, folder_id=folder_id, search_by=search_by
            )
            return spreadsheet
        except SpreadsheetNotFound as error:
            print(f"Spreadsheet not found. Error: {error}")
            return None
        except ValueError as error:
            print(error)
            return None
