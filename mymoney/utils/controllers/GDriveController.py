from typing import List
from mymoney.utils.clients.GDriveClient import GDriveClient
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource


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
        self._client: Resource = client.getClient()

    def listFolders(self) -> List:
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

    def newFolder(self, name: str, parent_id: str = None) -> dict:
        """
        Creates a new folder in Google Drive.

        :param name: The name of the new folder.
        :param parent_id: The ID of the parent folder (optional).
        :return: The metadata of the created folder.
        """
        folder_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            folder_metadata["parents"] = [parent_id]

        try:
            folder = (
                self._client.files()
                .create(body=folder_metadata, fields="id, name")
                .execute()
            )
            return folder
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def deleteFolder(self, folder_id: str) -> None:
        """
        Deletes a folder in Google Drive.

        :param folder_id: The ID of the folder to delete.
        """
        try:
            self._client.files().delete(fileId=folder_id).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def searchFolder(self, name: str) -> List[dict]:
        """
        Searches for folders by name.

        :param name: The name of the folder to search for.
        :return: A list of folder metadata that match the search query.
        """
        query = f"""name = '{name}' and
        "mimeType = 'application/vnd.google-apps.folder' and trashed = false"""
        try:
            results = (
                self._client.files().list(q=query, fields="files(id, name)").execute()
            )
            folders = results.get("files", [])
            return folders
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def listFolder(self, folder_id: str) -> List[dict]:
        """
        Lists the contents of a folder.

        :param folder_id: The ID of the folder to list.
        :return: A list of metadata for each file and folder in the specified folder.
        """
        query = f"'{folder_id}' in parents and trashed = false"
        try:
            results = (
                self._client.files()
                .list(q=query, fields="files(id, name, mimeType)")
                .execute()
            )
            items = results.get("files", [])
            return items
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def updateFolder(self, folder_id: str, new_name: str) -> dict:
        """
        Updates the name of a folder.

        :param folder_id: The ID of the folder to update.
        :param new_name: The new name for the folder.
        :return: The metadata of the updated folder.
        """
        folder_metadata = {"name": new_name}
        try:
            updated_folder = (
                self._client.files()
                .update(fileId=folder_id, body=folder_metadata, fields="id, name")
                .execute()
            )
            return updated_folder
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
