from gspread.client import Client


class BaseRepository:
    """
    Attributes:
        _client: The client for interacting with Google Sheets.
        _spreadsheet: The spreadsheet object.
        _worksheet: The current worksheet
    """

    def __init__(self, client: Client) -> None:
        self._client: Client = client
        self.nome = "aaa"
