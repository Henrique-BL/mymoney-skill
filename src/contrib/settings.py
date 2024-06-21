from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.Utils import Utils


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Alexa-MyMoneySkill Api"
    ROOT_PATH: str = ""

    MONGO_URI: str
    MONGO_DB: str
    CURRENT_COLLECTION: str

    GSPREAD_SCOPES: List[str]
    GSPREAD_CREDS_PATH: str

    GDRIVE_CREDS_PATH: str
    GDRIVE_SCOPES: List[str]

    GSHEET_SERVICE_ACCOUNT_EMAIL: str
    # Define the cell where metadata will be found
    METADATA_DEFAULT_INDEX: str
    # Initial row position of headers
    HEADERS_DEFAULT_ROW: int

    # All the headers, Type columns are used to control index outcome and income flow
    HEADERS: List[str]

    # Define position for every column of header, takes in consideration the Type column
    MONEY_COL: int
    DEBIT_COL: int
    CREDIT_COL: int
    BANK_COL: int
    PIX_COL: int

    # Initial row where data will be inserted in every empty columun
    DATA_ROW_DEFAULT: int

    # Default values of income and outcome
    INCOME_DEFAULT: int
    OUTCOME_DEFAULT: int

    # Status of creation
    CREATED_DEFAULT: bool

    # Current month
    CURRENT_MONTH: str = Utils.current_month()
    CURRENT_YEAR: str = str(Utils.current_utc_time().year)


settings = Settings()
