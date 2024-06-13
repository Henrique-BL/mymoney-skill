from gspread.spreadsheet import Spreadsheet
from gspread.client import Client
from gspread.exceptions import SpreadsheetNotFound

from mymoney.utils.exceptions.Exceptions import (
    FileAlreadyExistsException,
    FileNotFoundException,
)


class SpreadsheetController:
    @staticmethod
    def createSpreadsheet(gspread: Client, title: str, folder_id: str) -> str:
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

        try:
            if (
                SpreadsheetController.searchSpreadsheet(
                    gspread=gspread, identifier=title, folder_id=folder_id
                )
                is not None
            ):
                raise FileAlreadyExistsException(folder_id)

            spreadsheet: Spreadsheet = gspread.create(title=title, folder_id=folder_id)

            return spreadsheet.id
        except FileAlreadyExistsException as error:
            print(error)
            return None

    def searchSpreadsheet(
        gspread: Client, identifier: str, folder_id: str, search_by: str = "title"
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
                spreadsheet: Spreadsheet = gspread.open(
                    title=identifier, folder_id=folder_id
                )

            else:
                spreadsheet: Spreadsheet = gspread.open_by_key(id=identifier)

            return spreadsheet
        except SpreadsheetNotFound as error:
            print(f"Spreadsheet not found. Error: {error}")
            return None

    def deleteSpreadsheet(gspread: Client, title: str, folder_id: str) -> str:
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

        try:
            spreadsheet: Spreadsheet = SpreadsheetController.searchSpreadsheet(
                gspread=gspread, identifier=title, folder_id=folder_id
            )

            if spreadsheet is not None:
                gspread.del_spreadsheet(file_id=spreadsheet.id)
                return spreadsheet.id

            else:
                raise FileNotFoundException(file_id=title)

        except FileNotFoundException as error:
            print(error)
            return None

    def updateSpreadsheet(
        gspread: Client, title: str, new_title: str, folder_id: str
    ) -> str:
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
        try:
            spreadsheet: Spreadsheet = SpreadsheetController.searchSpreadsheet(
                gspread=gspread, identifier=new_title, folder_id=folder_id
            )

            if spreadsheet is not None:
                raise FileAlreadyExistsException(new_title)

            spreadsheet: Spreadsheet = SpreadsheetController.searchSpreadsheet(
                gspread=gspread, identifier=title, folder_id=folder_id
            )

            if spreadsheet is not None:
                spreadsheet.update_title(new_title)
                return spreadsheet.id

            else:
                raise FileNotFoundException(file_id=title)

        except FileNotFoundException as error:
            print(error)
            return None
        except FileAlreadyExistsException as error:
            print(error)
            return None
