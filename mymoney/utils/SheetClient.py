from typing import List
from google.oauth2.service_account import Credentials
import gspread


class SheetClient:
    def __init__(self, scopes: List, path: str) -> None:
        self.path = path
        self.scopes = scopes
        self.creds: Credentials = Credentials.from_service_account_file(
            self.path, scopes=self.scopes
        )

    def getClient(self):
        return gspread.auth.authorize(self.creds)
