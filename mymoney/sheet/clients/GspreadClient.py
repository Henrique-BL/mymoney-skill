import gspread

from gspread.client import Client

from mymoney.contrib.settings import settings


class GspreadClient:
    def __init__(self) -> None:
        self._creds = settings.GSPREAD_CREDS_PATH

    def getClient(self) -> Client:
        return gspread.service_account(filename=self._creds)


client = GspreadClient()
