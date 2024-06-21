from src.contrib import settings


class MetadataUtil:
    @staticmethod
    def defaultMetadata() -> dict:
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
        return metadata
