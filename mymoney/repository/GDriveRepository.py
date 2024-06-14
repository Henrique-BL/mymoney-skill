import os
from typing import List
from googleapiclient.errors import HttpError
from googleapiclient.discovery import Resource
from mymoney.utils.exceptions.Exceptions import (
    FileAlreadyExistsException,
    FileNotFoundException,
)
from dotenv import load_dotenv

load_dotenv()


class GDriveRepository:
    """

    Attributes:
        _client: The client for interacting with Google Sheets.
        _spreadsheet: The spreadsheet object.
        _worksheet: The current worksheet
    """

    def __init__(self, client: Resource) -> None:
        """
        Initializes the SheetController with the specified
        spreadsheet name and GspreadClient.

        Args:
            spreadsheet (str): The name of the spreadsheet.
            client (GspreadClient): The client to interact with Google Sheets.
        """
        self._client: Resource = client

    def newFolder(self, name: str, parent_id: str = None) -> dict:
        """
        Creates a new folder in Google Drive.

        :param name: The name of the new folder.
        :param parent_id: The ID of the parent folder (optional).
        :return: The metadata of the created folder.
        """

        if self.searchFolder(identifier=name):
            raise FileAlreadyExistsException(name)

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

    def updateFolder(self, folder_id: str, new_name: str) -> dict:
        """
        Updates the name of a folder.

        :param folder_id: The ID of the folder to update.
        :param new_name: The new name for the folder.
        :return: The metadata of the updated folder.
        """

        if self.searchFolder(identifier=new_name):
            raise FileAlreadyExistsException(new_name)

        if not self.searchFolder(identifier=folder_id, search_by="id"):
            raise FileNotFoundException(folder_id)

        folder_metadata = {"name": new_name}
        try:
            updated_folder = (
                self._client.files()
                .update(fileId=folder_id, body=folder_metadata, fields="id, name")
                .execute()
            )
            return updated_folder
        except HttpError() as error:
            print(f"An error occurred: {error}")
            return None

    def deleteFolder(self, folder_id: str) -> None:
        """
        Deletes a folder in Google Drive.

        :param folder_id: The ID of the folder to delete.
        """

        if not self.searchFolder(identifier=folder_id, search_by="id"):
            raise FileNotFoundException(folder_id)

        try:
            self._client.files().delete(fileId=folder_id).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    def searchFolder(self, identifier: str, search_by: str = "title") -> List[dict]:
        """
        Searches for folders by name or id.

        :param identifier: The name or ID of the folder to search for.
        :param search_by: The type of search to perform ('title' or 'id').
        :return: A list of folder metadata that match the search query.
        """
        if search_by not in ["title", "id"]:
            raise ValueError("search_by must be 'title' or 'id'")

        try:
            if search_by == "title":
                query = f"name = '{identifier}' and mimeType = \
                'application/vnd.google-apps.folder' and trashed = false"
                results = (
                    self._client.files()
                    .list(q=query, fields="files(id, name)")
                    .execute()
                )
                folders = results.get("files", [])
            else:  # search_by == 'id'
                file = (
                    self._client.files()
                    .get(fileId=identifier, fields="id, name, mimeType, trashed")
                    .execute()
                )
                if (
                    file["mimeType"] == "application/vnd.google-apps.folder"
                    and not file["trashed"]
                ):
                    folders = [file]
                else:
                    folders = None

            return folders
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def shareFolder(
        self,
        folder_title: str,
        email_address: str = os.environ.get("GSHEET_SERVICE_ACCOUNT_EMAIL"),
    ) -> str:
        """
        Garant folder acess permission and write role to another user.

        :param folder_title: The title of the folder.
        :param email_adress: The user email to grant acess
        :return: The id of the shared folder
        """
        folder_id = self.searchFolder(folder_title)[0]["id"]
        try:
            permission = {
                "type": "user",
                "role": "writer",
                "emailAddress": email_address,
            }
            self._client.permissions().create(
                fileId=folder_id,
                body=permission,
                fields="id",
            ).execute()

            return folder_id
        except HttpError as error:
            print(f"An error occurred: {error}")

    def listFolders(self) -> List:
        """
        List all the folder of that the curent user has acess
        :return: list of all the folders (id,name)

        """
        folders = []
        page_token = None

        while True:
            try:
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
            except HttpError as error:
                print(f"A error as occur: {error}")
                return []

            for file in response.get("files", []):
                folders.append({"id": file.get("id"), "name": file.get("name")})

            page_token = response.get("nextPageToken", None)
            if not page_token:
                break

        return folders

    def listFiles(self, folder_id: str) -> List[dict]:
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
