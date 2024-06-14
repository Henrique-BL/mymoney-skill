from mymoney.services.GSheetService import GSheetService
from mymoney.repository.GDriveRepository import GDriveRepository

from gspread.spreadsheet import Spreadsheet
from mymoney.clients.GspreadClient import client as gspread_client
from mymoney.clients.GDriveClient import client as gdrive_client

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    gdrive = gdrive_client.getClient()
    gspread = gspread_client.getClient()

    drive_service = GDriveRepository(client=gdrive)
    sheet_service = GSheetService(client=gspread)

    # folder_id = drive_service.searchFolder("Relatorios")[0]["id"]

    # drive_service.newFolder(name="Test02",parent_id=folder_id)[0]

    # # drive_service.updateFolder(drive_service.searchFolder("Test")[0]["id"], "Bosta")
    # drive_service.deleteFolder(drive_service.searchFolder("Test")[0]["id"])

    folder_id = drive_service.searchFolder("Test02")[0]["id"]

    # drive_service.deleteFolder('18or07fp50T4NoYZsi-31YjUdmutLdHLl')
    print(drive_service.listFolders())

    # sheet_service._newSpreadsheet(title="test03",folder_id=folder_id)

    # sheet_service._worksheet._initialize()
    spreadsheet: Spreadsheet = sheet_service._searchSpreadSheet("test03", folder_id)
    # sheet_service._setCurrentSpreadsheet()
    sheet_service._setWorksheet(spreadsheet.sheet1)
    # sheet_service._worksheet._insertCell(40, "Outcome", "Money")
    # sheet_service._worksheet._insertCell(40, "Outcome", "Money")

    sheet_service._worksheet._deleteLastCell("Money")
