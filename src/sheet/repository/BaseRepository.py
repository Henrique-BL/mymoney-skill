from gspread.client import Client

from src.sheet.clients.GspreadClient import client


class BaseRepository:
    """
    Attributes:
        _client: The client for interacting with Google Sheets.
        _spreadsheet: The spreadsheet object.
        _worksheet: The current worksheet
    """

    def __init__(self) -> None:
        self._client: Client = client.getClient()
