import json
from gspread.worksheet import Worksheet


class MetadataController:
    @staticmethod
    def defineMetadata(worksheet: Worksheet) -> None:
        """
        Initializes the metadata with default values for various financial columns.
        """
        metadata = {
            "Money": {"index": 1, "last": 3},
            "Debit Card": {"index": 3, "last": 3},
            "Credit Card": {"index": 5, "last": 3},
            "Bank Transfer": {"index": 7, "last": 3},
            "Pix": {"index": 9, "last": 3},
            "Income": 0,
            "Outcome": 0,
            "Created": False,
        }
        worksheet.update_acell("A1", json.dumps(metadata))

    @staticmethod
    def getMetadata(worksheet: Worksheet) -> dict:
        """
        Retrieves metadata from the first cell (A1) and converts it to a dictionary.

        Returns:
            dict: The metadata dictionary.
        """
        data = worksheet.acell("A1").value
        metadata = json.loads(data)
        return metadata

    @staticmethod
    def updateMetadata(
        worksheet: Worksheet, metadata: dict, type: str | None, value: float | None
    ) -> None:
        """
        Updates the metadata in cell A1 after insert, update, or delete actions.

        Args:
            metadata (dict): The metadata dictionary.
            type (str | None): The type of transaction ("Income" or "Outcome").
            value (float | None): The transaction amount.
        """

        if type == "Income":
            metadata["Income"] += value
        elif type == "Outcome":
            metadata["Outcome"] += value

        worksheet.update_acell("A1", json.dumps(metadata))
