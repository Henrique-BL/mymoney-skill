from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from mymoney.contrib.settings import settings


class GDriveClient:
    def __init__(self) -> None:
        self._path = settings.GDRIVE_CREDS_PATH
        self._scopes = settings.GDRIVE_SCOPES

        self._creds: Credentials = Credentials.from_service_account_file(
            filename=self._path, scopes=self._scopes
        )

    def getClient(self) -> Resource:
        return build(serviceName="drive", version="v3", credentials=self._creds)


client = GDriveClient().getClient()
