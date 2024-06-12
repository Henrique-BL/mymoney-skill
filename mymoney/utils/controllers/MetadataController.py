import json
from gspread.worksheet import Worksheet
from mymoney.contrib import settings


class MetadataController:
    @staticmethod
    def defineMetadata(worksheet: Worksheet) -> None:
        """
        Initializes the metadata with default values for various financial columns.
        """
        metadata = {
            "Money": {"index": settings.MONEY_COL, "last": settings.DATA_ROW_DEFAULT},
            "Debit Card": {
                "index": settings.DEBIT_COL,
                "last": settings.DATA_ROW_DEFAULT,
            },
            "Credit Card": {
                "index": settings.CREDIT_COL,
                "last": settings.DATA_ROW_DEFAULT,
            },
            "Bank Transfer": {
                "index": settings.BANK_COL,
                "last": settings.DATA_ROW_DEFAULT,
            },
            "Pix": {"index": settings.PIX_COL, "last": settings.DATA_ROW_DEFAULT},
            "Income": settings.INCOME_DEFAULT,
            "Outcome": settings.OUTCOME_DEFAULT,
            "Created": settings.CREATED_DEFAULT,
        }
        worksheet.update_acell(settings.METADATA_DEFAULT_INDEX, json.dumps(metadata))

    @staticmethod
    def getMetadata(worksheet: Worksheet) -> dict:
        """
        Retrieves metadata from the first cell (A1) and converts it to a dictionary.

        Returns:
            dict: The metadata dictionary.
        """
        data = worksheet.acell(settings.METADATA_DEFAULT_INDEX).value
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

        worksheet.update_acell(settings.METADATA_DEFAULT_INDEX, json.dumps(metadata))
