class BaseExcpetion(Exception):
    def __init__(self, message) -> None:
        self._message: str = message

    def message(self) -> str:
        return self._message


class FolderAlreadyExistsException(BaseException):
    def __init__(self, folder_name: str) -> None:
        self.message = f"Folder {folder_name} already exists in current directory,\
        try another title."
        super().__init__(self.message)


class FolderNotFoundException(BaseException):
    def __init__(self, folder_id) -> None:
        self.message = f"Folder not found with given id. ID: {folder_id}."
        super().__init__(self.message)
