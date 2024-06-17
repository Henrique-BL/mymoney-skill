from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Alexa-MyMoneySkill Api"
    ROOT_PATH: str = "/"
    MONGO_URI: str
    MONGO_DB: str
    CURRENT_COLLECTION: str

    # GSPREAD_SCOPES : str
    # GSPREAD_CREDS_PATH  : str

    # GDRIVE_CREDS_PATH  : str
    # GDRIVE_SCOPES  : str

    # GSHEET_SERVICE_ACCOUNT_EMAIL  : str
    # # Define the cell where metadata will be found
    # METADATA_DEFAULT_INDEX : str
    # # Initial row position of headers
    # HEADERS_DEFAULT_ROW : str

    # # All the headers, Type columns are used to control index outcome and income flow
    # HEADERS :str

    # # Define position for every column of header, takes in consideration the Type
    # column
    # MONEY_COL : str
    # DEBIT_COL : str
    # CREDIT_COL : str
    # BANK_COL : str
    # PIX_COL : str

    # # Initial row where data will be inserted in every empty columun
    # DATA_ROW_DEFAULT : str

    # # Default values of income and outcome
    # INCOME_DEFAULT : str
    # OUTCOME_DEFAULT : str

    # # Status of creation
    # CREATED_DEFAULT : bool

    # # Current month
    # CURRENT_MONTH : str
    # # Current year
    # CURRENT_YEAR  : str


settings = Settings()
