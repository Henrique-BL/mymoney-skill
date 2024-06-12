class BaseExcpetion(Exception):
    def __init__(self, message) -> None:
        self._message: str = message

    def message(self) -> str:
        return self._message
