from typing import List, Optional
from mymoney.sheet.exceptions.Exceptions import (
    FileAlreadyExistsException,
    FileNotFoundException,
)
from mymoney.sheet.repository.GDriveRepository import GDriveRepository


class GDriveService:
    def __init__(self) -> None:
        self._repository = GDriveRepository()

    def newFolder(self, name: str, dir: str = None) -> Optional[dict]:
        data: dict = None
        try:
            data = self._repository.newFolder(name, dir)

        except FileAlreadyExistsException as error:
            print(error)

        finally:
            return data

    def searchFolder(self, identifier: str, search_by: str = "title") -> Optional[List]:
        """
        Searches for folders by name or id.

        :param identifier: The name or ID of the folder to search for.
        :param search_by: The type of search to perform ('title' or 'id').
        :return: A list of folder metadata that match the search query.
        """
        folders: List[dict] = None
        try:
            folders: List[dict] = self._repository.searchFolder(identifier, search_by)
        except ValueError as error:
            print(error)
        except FileNotFoundException as error:
            print(error)
        finally:
            return folders

    def updateFolder(self, folder_id: str, new_name: str) -> dict:
        """
        Updates the name of a folder.

        :param folder_id: The ID of the folder to update.
        :param new_name: The new name for the folder.
        :return: The metadata of the updated folder.
        """
        folder_updated: dict = None
        try:
            folder_updated = self._repository.updateFolder(folder_id, new_name)
        except FileAlreadyExistsException as error:
            print(error)
        except FileNotFoundException as error:
            print(error)
        finally:
            return folder_updated

    def deleteFolder(self, folder_id: str) -> None:
        """
        Deletes a folder in Google Drive.

        :param folder_id: The ID of the folder to delete.
        """
        try:
            self._client.files().delete(fileId=folder_id).execute()
        except FileNotFoundException as error:
            print(error)

    def shareFolder(self, folder: str) -> Optional[str]:
        self._repository.shareFolder(folder)

    def listFolders(self) -> Optional[List]:
        return self._repository.listFolders()

    def listFiles(self, folder: str) -> Optional[List]:
        return self._repository.listFiles(folder)
