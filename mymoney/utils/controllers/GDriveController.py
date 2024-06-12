from typing import List
from mymoney.utils.clients.GDriveClient import GDriveClient


class GDriveController:
    """

    Attributes:
        _client: The client for interacting with Google Sheets.
        _spreadsheet: The spreadsheet object.
        _worksheet: The current worksheet
    """

    def __init__(self, client: GDriveClient) -> None:
        """
        Initializes the SheetController with the specified
        spreadsheet name and GspreadClient.

        Args:
            spreadsheet (str): The name of the spreadsheet.
            client (GspreadClient): The client to interact with Google Sheets.
        """
        self._client = client.getClient()

    def list_folders(self) -> List:
        folders = []
        page_token = None

        while True:
            response = (
                self._client.files()
                .list(
                    q="mimeType='application/vnd.google-apps.folder'",
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )

            for file in response.get("files", []):
                folders.append({"id": file.get("id"), "name": file.get("name")})

            page_token = response.get("nextPageToken", None)
            if not page_token:
                break
        return folders
