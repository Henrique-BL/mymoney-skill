from mymoney.utils.controllers.GSheetController import GSheetController
from mymoney.utils.controllers.GDriveController import GDriveController

from mymoney.utils.clients.GspreadClient import client as gspread_client
from mymoney.utils.clients.GDriveClient import client as gdrive_client
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    gdrive = gdrive_client.getClient()
    gspread = gspread_client.getClient()

    drive_controller = GDriveController(client=gdrive)

    sheet_controller = GSheetController("test_sheet", client=gspread)

    sheet_controller.newSheet(
        title="test01", folder_id=drive_controller.shareFolder("Planilhas")
    )

    breakpoint()
    sheet_controller.initialize()
    sheet_controller.insertCell(40, "Outcome", "Money")
    sheet_controller.insertCell(40, "Outcome", "Money")
    sheet_controller.deleteLastCell("Money")
