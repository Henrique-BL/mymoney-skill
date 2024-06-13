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
    sheet_controller = GSheetController(client=gspread)

    folder_id = drive_controller.searchFolder("Relatorios")[0]["id"]


"""
    breakpoint()
    sheet_controller.initialize()
    sheet_controller.insertCell(40, "Outcome", "Money")
    sheet_controller.insertCell(40, "Outcome", "Money")
    sheet_controller.deleteLastCell("Money")
"""
