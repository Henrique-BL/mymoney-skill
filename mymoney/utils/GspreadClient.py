import os
import gspread

from dotenv import load_dotenv

load_dotenv()


class GspreadClient:
    def __init__(self) -> None:
        self._path = os.environ.get("KEY_PATH")
        self._client = gspread.service_account(filename=self._path)

    def getClient(self):
        return self._client


client = GspreadClient()
