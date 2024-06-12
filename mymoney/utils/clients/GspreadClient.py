import os
import gspread

from dotenv import load_dotenv

load_dotenv()


class GspreadClient:
    def __init__(self) -> None:
        self._creds = os.environ.get("GSPREAD_CREDS_PATH")
        self._client = gspread.service_account(filename=self._creds)

    def getClient(self):
        return self._client


client = GspreadClient()
