from gspread.spreadsheet import Spreadsheet
from src.sheet.repository.BaseRepository import BaseRepository
from src.sheet.exceptions.Exceptions import (
    FileAlreadyExistsException,
    FileNotFoundException,
)
from gspread.exceptions import SpreadsheetNotFound


class SpreadsheetRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__()

    def _createSpreadsheet(self, title: str, folder_id: str) -> str:
        """
        Creates a new Spreasheet in the folder passed as parameter

        Args:
            gspread (gspread.client): The gspread client.
            title (str): The title of the spreadsheet
            folder_id (str): The folder_id of the destination folder

        Returns:
            str: The id of the inserted spreasheet
            None: if spreadsheet with given title already exists in the folder
        """
        if self._searchSpreadsheet(identifier=title, folder_id=folder_id) is not None:
            raise FileAlreadyExistsException(title)

        spreadsheet: Spreadsheet = self._client.create(title=title, folder_id=folder_id)

        return spreadsheet.id

    def _searchSpreadsheet(
        self, identifier: str, folder_id: str, search_by: str = "title"
    ) -> Spreadsheet:
        """
        Search for a  Spreasheet in the folder passed as parameter

        Args:
            gspread (gspread.client): The gspread client.
            identifier (str): The title or id of the spreadsheet
            folder_id (str): The folder_id of the destination folder
            search_by (str): The search method, default 'title'

        Returns:
            gspread.Spreadsheet: The spreasheet object of the searched
            None: If no spreadsheet are found
        """

        if search_by not in ["title", "id"]:
            raise ValueError("search_by must be 'title' or 'id'")

        try:
            if search_by == "title":
                spreadsheet: Spreadsheet = self._client.open(
                    title=identifier, folder_id=folder_id
                )

            else:
                spreadsheet: Spreadsheet = self._client.open_by_key(key=identifier)

            return spreadsheet
        except SpreadsheetNotFound:
            return None

    def _deleteSpreadsheet(self, title: str, folder_id: str) -> str:
        """
        Remove a Spreasheet in the folder passed as parameter

        Args:
            gspread (gspread.client): The gspread client.
            title (str): The title of the spreadsheet
            folder_id (str): The folder_id of the destination folder

        Returns:
            str: The id of the inserted spreasheet
            None: If spreadsheet with given title does'nt exists in the folder
        """

        spreadsheet: Spreadsheet = self._searchSpreadsheet(
            identifier=title, folder_id=folder_id
        )

        if spreadsheet is not None:
            self._client.del_spreadsheet(file_id=spreadsheet.id)
            return spreadsheet.id

        else:
            raise FileNotFoundException(file_id=title)

    def _updateSpreadsheet(self, title: str, new_title: str, folder_id: str) -> str:
        """
        Update the name of a Spreasheet in the folder passed as parameter

        Args:
            gspread (gspread.client): The gspread client.
            title (str): The title of the spreadsheet
            new_title (str): The new title for the spreadsheet

            folder_id (str): The folder_id of the destination folder

        Returns:
            str: The id of the inserted spreasheet
            None: If spreadsheet with given title does'nt exists in the folder
        """

        spreadsheet: Spreadsheet = self._searchSpreadsheet(
            identifier=new_title, folder_id=folder_id
        )

        if spreadsheet is None:
            spreadsheet: Spreadsheet = self._searchSpreadsheet(
                identifier=title, folder_id=folder_id
            )

            if spreadsheet is not None:
                spreadsheet.update_title(new_title)
                return spreadsheet.id
            else:
                raise FileNotFoundException(file_id=title)
        else:
            raise FileAlreadyExistsException(new_title)
