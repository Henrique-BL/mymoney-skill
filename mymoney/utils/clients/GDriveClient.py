import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
import ast
from dotenv import load_dotenv

load_dotenv()


class GDriveClient:
    def __init__(self) -> None:
        self._path = os.environ.get("GDRIVE_CREDS_PATH")
        self._scopes = ast.literal_eval(os.environ.get("GDRIVE_SCOPES"))

        self._creds: Credentials = Credentials.from_service_account_file(
            filename=self._path, scopes=self._scopes
        )
        self._client: Resource = build("drive", "v3", credentials=self._creds)

    def getClient(self):
        return self._client


client = GDriveClient()