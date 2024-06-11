import datetime
import json
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from mymoney.utils.GspreadClient import GspreadClient


class SheetController:
    def __init__(self, spreadsheet: str, client: GspreadClient) -> None:
        self._client = client.getClient()
        self._spreadsheet: Spreadsheet = self._client.open(spreadsheet)
        self._worksheet: Worksheet | None = self._spreadsheet.worksheet("6")

    # Create worksheet with the currently year
    def newWorksheet(self):
        self._worksheet = self._spreadsheet.add_worksheet(
            str(datetime.datetime.now().month), 100, 20
        )

    # Initalize all the spreadsheet fields
    def initialize(self):
        self.newWorksheet()
        self.initializeMetadata()

        headers = [
            "Money",
            "Type",
            "Debit Card",
            "Type",
            "Credit Card",
            "Type",
            "Bank transfer",
            "Type",
            "Pix",
            "Type",
        ]
        self._worksheet.insert_row(headers, 2)

    # Get metadata from line 1 and convert it to dict and return it
    def getMetadata(self) -> dict:
        data = self._worksheet.acell("A1").value

        metadata = json.loads(data)

        return metadata

    def initializeMetadata(self):
        metadata = {
            "Money": {"index": 1, "last": 3},
            "Debit": {"index": 3, "last": 3},
            "Credit": {"index": 5, "last": 3},
            "Bank": {"index": 7, "last": 3},
            "Pix": {"index": 9, "last": 3},
        }

        self._worksheet.update_acell("A1", json.dumps(metadata))

    def updateMetadata(self, metadata):
        self._worksheet.update_acell("A1", json.dumps(metadata))

    # !Attention to case-sensitve column name
    def insertData(self, data: float, type: str, column: str) -> None:
        metadata = self.getMetadata()

        col: dict = metadata.get(column)

        row = col.get("last")
        self._worksheet.update_cell(row=row, col=col.get("index"), value=data)
        self._worksheet.update_cell(row=row, col=col.get("index") + 1, value=type)

        col["last"] = row + 1

        self.updateMetadata(metadata=metadata)
