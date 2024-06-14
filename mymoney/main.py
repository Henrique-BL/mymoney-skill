from mymoney.services.GSheetService import GSheetService
from mymoney.repository.GDriveRepository import GDriveRepository

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

    # drive_service.newFolder(name="Test",parent_id=folder_id)[0]

    folder_id = drive_service.searchFolder("Test")[0]["id"]

    # drive_service.deleteFolder('18or07fp50T4NoYZsi-31YjUdmutLdHLl')
    # print(drive_service.listFolders())
    # folder_id = drive_service.searchFolder("Planilhas")[0]["id"]

    # csheet_service.newSpreadsheet(title="test02",folder_id=folder_id)
    # sheet_service.setSpreadsheet(spreadsheet)
    spreadsheet = sheet_service.searchSpreadSheet(
        identifier="Test2", folder_id=folder_id
    )

    sheet_service._service.setWorkheet(spreadsheet.sheet1)
    sheet_service._service.initialize()

    # sheet_service._service.insertCell(40, "Outcome", "Money")
    # sheet_service._service.insertCell(40, "Outcome", "Money")

# sheet_service._service.deleteLastCell("Money")
