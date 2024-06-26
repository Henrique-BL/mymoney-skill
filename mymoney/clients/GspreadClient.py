import os
import gspread

from gspread.client import Client


class GspreadClient:
    def __init__(self) -> None:
        self._creds = os.environ.get("GSPREAD_CREDS_PATH")

    def getClient(self) -> Client:
        return gspread.service_account(filename=self._creds)


client = GspreadClient()
