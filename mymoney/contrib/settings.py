import datetime


METADATA_DEFAULT_INDEX = "N1"  # Define the cell where metadata will be found
HEADERS_DEFAULT_ROW = 1  # Initial row position of headers

# All the headers, Type columns are used to control index outcome and income flow
HEADERS = [
    "Money",
    "Type",
    "Debit Card",
    "Type",
    "Credit Card",
    "Type",
    "Bank Transfer",
    "Type",
    "Pix",
    "Type",
]
# Define position for every column of header, takes in consideration the Type column
MONEY_COL = 1
DEBIT_COL = 3
CREDIT_COL = 5
BANK_COL = 7
PIX_COL = 9

# Initial row where data will be inserted in every empty columun
DATA_ROW_DEFAULT = 2

# Default values of income and outcome
INCOME_DEFAULT = 0
OUTCOME_DEFAULT = 0

# Status of creation
CREATED_DEFAULT = False

# Current month
CURRENT_MONTH = str(datetime.datetime.now().month)
# Current year
CURRENT_YEAR = str(datetime.datetime.now().year)
