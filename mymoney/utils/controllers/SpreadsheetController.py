from gspread.spreadsheet import Spreadsheet
from gspread.client import Client
from gspread.exceptions import SpreadsheetNotFound


class SpreadsheetController:
    @staticmethod
    def createSpreadsheet(gspread: Client, title: str, folder_id) -> str:
        if SpreadsheetController.searchSpreadsheet(
            gspread=gspread, title=title, folder_id=folder_id
        ):
            raise Exception

        try:
            spreadsheet: Spreadsheet = gspread.create(title=title, folder_id=folder_id)

            return spreadsheet.id

        except Exception as error:
            print(error)
            return None

    def searchSpreadsheet(gspread: Client, title: str, folder_id) -> str:
        try:
            spreadsheet: Spreadsheet = gspread.open(title=title, folder_id=folder_id)

            return spreadsheet

        except SpreadsheetNotFound as error:
            print(f"An error as occour: {error}")
            return None

    def deleteSpreadsheet(gspread: Client, title: str, folder_id) -> str:
        try:
            spreadsheet: Spreadsheet = SpreadsheetController.searchSpreadsheet(
                gspread=gspread, title=title, folder_id=folder_id
            )
            if spreadsheet:
                gspread.del_spreadsheet(file_id=spreadsheet.id)
                return spreadsheet.id
            else:
                print("AAAAAAAAAAAAa")
                raise FileNotFoundError()

        except Exception as error:
            print(error)
            return None

    def updateSpreadsheet(gspread: Client, title: str, folder_id) -> str:
        try:
            spreadsheet: Spreadsheet = gspread.create(title=title, folder_id=folder_id)

            return spreadsheet.id
        except Exception as error:
            print(error)
