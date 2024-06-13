class BaseExcpetion(Exception):
    def __init__(self, message) -> None:
        self._message: str = message

    def message(self) -> str:
        return self._message


class FileAlreadyExistsException(BaseException):
    def __init__(self, file_name: str) -> None:
        self.message = f"File {file_name} already exists in current directory,\
        try another title."
        super().__init__(self.message)


class FileNotFoundException(BaseException):
    def __init__(self, file_id) -> None:
        self.message = f"File not found with given id. ID: {file_id}."
        super().__init__(self.message)
